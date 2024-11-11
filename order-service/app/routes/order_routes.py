from fastapi import APIRouter
from app.crud.order_crud import get_product_availability, get_product_data, add_in_cart
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