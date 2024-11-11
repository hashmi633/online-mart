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
        cart_item.quantity += quantity
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

