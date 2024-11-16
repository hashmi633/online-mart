from fastapi import APIRouter
from app.crud.order_crud import get_product_availability, get_product_data, add_in_cart, view_of_cart, delete_in_cart, update_of_cart, order_creation
from app.models.order_models import Cart
from app.order_db.db_connector import DB_SESSION

router = APIRouter()

@router.get('/')
def welcome():
    return {"Welcome to Order Service"}

@router.get('/product_availability')
def inventory_quantity(id: int):
    quantity = get_product_availability(id)
    return quantity

@router.get('/product-updates')
def product_data(id: int):
    data = get_product_data(id)
    return data

@router.post("/add-to-cart")
def add_to_cart(cart: Cart, product_id: int, quantity: int, session: DB_SESSION):
    cart = add_in_cart(cart, product_id, quantity, session)
    return cart

@router.get("/view-cart")
def view_cart(cart_id : int, session: DB_SESSION):
    cart = view_of_cart(cart_id, session)
    return cart

@router.delete("/delete-item-from-cart")
def delete_from_cart(product_id: int, cart_id: int, session: DB_SESSION):
    delete_item = delete_in_cart(product_id, cart_id, session)
    return delete_item

@router.put('/update-cart')
def update_cart(product_id: int, cart_id: int, quantity: int, session: DB_SESSION):
    cart = update_of_cart(product_id, cart_id, quantity, session)
    return cart

@router.post('/create-order')
def create_order(cart_id: int, user_id: int, session: DB_SESSION):
    order = order_creation(cart_id, user_id, session)
    return order