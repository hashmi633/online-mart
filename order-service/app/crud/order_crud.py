from app.order_kafka.order_consumers import inventory_cache, product_cache, consume_product_responses, consume_product_quantity_responses
from sqlmodel import Session, select
from fastapi import HTTPException
from app.models.order_models import Cart, CartItem, OrderItem, Order
from aiokafka import AIOKafkaProducer
import json
import logging

def get_product_availability(id: int):
    inventory_from_cache = inventory_cache.get(id)
    if inventory_from_cache is None:
        raise HTTPException(
            status_code=404,
        detail="item not found in cache"
        )
    else:
        return inventory_from_cache

def get_product_data(id: int):
    product_from_cache = product_cache.get(id)
    if product_from_cache is None:
        raise HTTPException(
            status_code=404,
        detail="product not found in cache"
        )
    else:
        return product_from_cache

def add_in_cart(cart: Cart, product_id : int, quantity : int, session: Session):
    # Step 0: Restrict zero or negative quantities
    if quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than zero"
        )

    # Step 1: Check if there’s already an existing cart for the user/session
    existing_cart = session.exec(select(Cart).where(Cart.user_id == cart.user_id)).first()
    if existing_cart:
    # Use the existing cart if found
        cart = existing_cart
    else:
    # Create a new cart entry if no existing cart is found
        session.add(cart)
        session.commit()  # Commit to generate a cart_id
        session.refresh(cart)  # Refresh to get the generated cart_id
    
    # Step 1: Check if product information is cached
    cached_product_data = get_product_data(product_id)
    cached_product_availability = get_product_availability(product_id)

    # Placeholder data if cache retrieval 
    product_name = cached_product_data.get("product_name") if cached_product_data else "Unknown Product"
    unit_price = cached_product_data.get("price") if cached_product_data else 0.0
    available_quantity = cached_product_availability.get("quantity") if cached_product_availability else 0

    # Step 4: Check if the requested quantity is available
    if quantity > available_quantity:
        raise HTTPException(
            status_code=400,
            detail="Insufficient stock available"
        ) 
    
    # Step # 5 Add or update the item in the cart
    cart_item = session.exec(select(CartItem).where(CartItem.cart_id == cart.cart_id, CartItem.product_id == product_id)).first()
    if cart_item:
        cart_item.quantity = quantity
        cart_item.unit_price = unit_price
    else:
    # Add new item to cart
        cart_item = CartItem(
            cart_id=cart.cart_id,
            product_id=product_id,
            product_name=product_name,
            unit_price=unit_price,
            quantity=quantity
        )
        session.add(cart_item)
    
    session.commit()
    session.refresh(cart_item)
    return cart_item

def update_of_cart(product_id: int, user_id: int, quantity: int, session: Session):
    # Retrieve the cart item by product_id and cart_id
    cart_item = session.exec(
        select(CartItem).where(CartItem.cart.user_id == user_id, CartItem.product_id == product_id)
    ).first()

    if not cart_item:
        raise HTTPException(
            status_code=404,
            detail="Product not found in cart"
        )
    # Update quantity or remove item if quantity is zero
    if quantity > 0:
        cart_item.quantity = quantity
        message= "Item quantity updated"
    else:
        # Remove item from cart if quantity is zero
        session.delete(cart_item)
        message= "Item removed from cart"
    
    # Commit changes and refresh the session
    session.commit()
    session.refresh(cart_item) if quantity > 0 else None # Only refresh if item still exists
    
    return {"message": message, "cart_item": cart_item if quantity > 0 else None}

def delete_in_cart(product_id: int, user_id: int, session: Session):
    # Retrieve the cart item by product_id and cart_id
    cart_item = session.exec(select(CartItem).where(CartItem.cart.user_id==user_id, CartItem.product_id==product_id)).first()
    if not cart_item:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    
    # Delete the cart item and commit changes
    session.delete(cart_item)
    session.commit()
    
    return {"message": "Item deleted successfully"}

def view_of_cart(user_id : int, session : Session):
    cart = session.exec(select(Cart).where(Cart.user_id== user_id)).first()
    if not cart:
        raise HTTPException(
            status_code=404,
            detail="Cart not found"
        )
    cart_items = session.exec(select(CartItem).where(CartItem.cart_id==cart.cart_id)).all()
    total_price = sum(item.quantity * item.unit_price for item in cart_items)

    return{
        "cart_id": cart.cart_id,
        "items": [
            {
                "product_id": item.product_id,
                "product_name": item.product_name,
                "unit_price": item.unit_price,
                "quantity": item.quantity,
                "total_price": item.unit_price * item.quantity
            } for item in cart_items
        ],
        "total_price": total_price
    }

async def order_creation(user_id: int, session: Session, producer: AIOKafkaProducer):
    # Step 1: Retrieve the cart and its items
    cart = session.exec(select(Cart).where(Cart.user_id==user_id)).first()
    if not cart:
        raise HTTPException(
            status_code=404,
            detail="Cart not found"
        )
    
    cart_items = session.exec(select(CartItem).where(CartItem.cart_id==cart.cart_id)).all()
    if not cart_items:
        raise HTTPException(
            status_code=400,
            detail="Cart is empty"
        )
    
    logging.info(f"Retrieved {len(cart_items)} items from the cart.")
    
    # Step 2: Collect all product IDs from the cart
    products_id = [item.product_id for item in cart_items]
    logging.info(f"Collected product IDs: {products_id}")
    
    # Step 3: Request product details from Product Service via Kafka
    request_data = {"product_ids": products_id}
    await producer.send_and_wait("get_product_details", json.dumps(request_data).encode("utf-8"))
    
    # Step 4: Wait for product details from Kafka response
    logging.info("Waiting for product details response from Kafka...")
    product_details = await consume_product_responses()
    product_quantity_details = await consume_product_quantity_responses()
    if not product_details or not product_quantity_details:
        raise HTTPException(
            status_code=400,
            detail="Failed to retrieve product details"
        )
    
    logging.info("Successfully retrieved product details and inventory quantities.")

    # Step 2: Initialize order details
    total_price = 0
    items_data = []
    logging.info("Validating inventory and finalizing order items...")
    # Step 3: Validate inventory and finalize order items
    for item in cart_items:    
        product = next((p for p in product_details if p['product_id'] == item.product_id), None)
        if not product:
            raise HTTPException(
                status_code=400,
                detail=f"Product with ID {item.product_id} not found in Product Service"
            )      

        product_quantity = next((p for p in product_quantity_details if p['product_id'] == item.product_id), None) 
        if not product_quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Product with ID {item.product_id} not found in Inventory Service"
            )      
        print(product_quantity.get("quantity"))
        # Check quantity
        if item.quantity > product_quantity.get("quantity", 0):
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for product {item.product_id}"
                )
        
        # Finalize item price and add to order total    
        item_price = product.get("price", 0.0)
        total_price += item.quantity * item_price
        
        # Prepare order item data

        item_data = {
            "product_id" : item.product_id,
            "product_name" : product["product_name"],
            "unit_price" : item_price,
            "quantity" : item.quantity
        }

        items_data.append(item_data)
        logging.info(f"Finalized item data for product_id={item.product_id}: {item_data}")

    # Step 4: Create Order entry
    logging.info("Creating order entry in the database...")
    order = Order(
        user_id = user_id,
        status = "pending",
        total_price= total_price
    )
    session.add(order)
    session.commit()
    session.refresh(order) 
    logging.info(f"Order created successfully with order_id={order.order_id}")

    inventory = []
    # Step 5: Add Order Items to Order
    for item_data in items_data:
        order_item = OrderItem(
            order_id = order.order_id,
            product_id= item_data.get("product_id"),
            product_name= item_data.get("product_name"),
            unit_price= item_data.get("unit_price"),
            quantity= item_data.get("quantity")
        )
        session.add(order_item)
        
        # Step 6: Deduct inventory levels and clear the cart
        inventory_deduction = {
            "product_id": order_item.product_id,
            "quantity": order_item.quantity
        }
        inventory.append(inventory_deduction)
    
    logging.info(f"Prepared inventory deduction data: {inventory}")
    try:
        logging.info("Sending inventory deduction request to Kafka...")
        await producer.send_and_wait("inventory_deduction", json.dumps({"products": inventory}).encode('utf-8'))
        logging.info("Inventory deduction request sent successfully.")
    except Exception as e:
        logging.error(f"Failed to send inventory deduction message: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to deduct inventory levels. Please try again."
        )    
    # Clear the cart and its items
    session.query(CartItem).filter(CartItem.cart_id == cart.cart_id).delete()  # Delete all cart items
    session.delete(cart)
    
    # Commit all changes in one transaction
    session.commit()

    return {"message": "Order created successfully", "order_id": order.order_id}

def all_orders(user_id: int , session : Session):
    orders = session.exec(select(Order).where(Order.user_id==user_id)).all()
    return orders

def all_carts(session: Session):
    carts = session.exec(select(Cart)).all()
    all_carts = [
        {
            "cart_id": cart.cart_id,
            "user_id": cart.user_id,
            "items": [item for item in cart.items] if hasattr(cart, "items") else []
        }
        for cart in carts
    ]

    return all_carts