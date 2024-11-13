from app.order_kafka.order_consumers import inventory_cache, product_cache
from sqlmodel import Session, select
from fastapi import HTTPException
from app.models.order_models import Cart, CartItem

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

def update_of_cart(product_id: int, cart_id: int, quantity: int, session: Session):
    # Retrieve the cart item by product_id and cart_id
    cart_item = session.exec(
        select(CartItem).where(CartItem.cart_id == cart_id, CartItem.product_id == product_id)
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

def delete_in_cart(product_id: int, cart_id: int, session: Session):
    # Retrieve the cart item by product_id and cart_id
    cart_item = session.exec(select(CartItem).where(CartItem.cart_id==cart_id, CartItem.product_id==product_id)).first()
    if not cart_item:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    
    # Delete the cart item and commit changes
    session.delete(cart_item)
    session.commit()
    
    return {"message": "Item deleted successfully"}

def view_of_cart(cart_id : int, session : Session):
    cart = session.get(Cart, cart_id)
    if not cart:
        raise HTTPException(
            status_code=404,
            detail="Cart not found"
        )
    cart_items = session.exec(select(CartItem).where(CartItem.cart_id==cart_id)).all()
    total_price = sum(item.quantity * item.unit_price for item in cart_items)

    return{
        "cart_id": cart_id,
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