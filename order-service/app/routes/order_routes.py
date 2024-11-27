from fastapi import APIRouter, Depends
from app.crud.order_crud import get_product_availability, get_product_data, add_in_cart, view_of_cart, delete_in_cart, update_of_cart, order_creation, signedin_user_orders, all_carts, all_orders, user_orders
from app.models.order_models import Cart
from app.order_db.db_connector import DB_SESSION
from app.order_kafka.order_consumers import get_kafka_producer
from typing import Annotated
from aiokafka import AIOKafkaProducer
from app.oath2 import validate_token, admin_validate_token

router = APIRouter()

@router.get('/')
def welcome():
    return {"Welcome to Order Service"}

@router.get('/product_availability', tags=["Product"])
def inventory_quantity(id: int):
    quantity = get_product_availability(id)
    return quantity

@router.get('/product-updates', tags=["Product"])
def product_data(id: int):
    data = get_product_data(id)
    return data

@router.post("/add-to-cart", tags=["Cart"])
def add_to_cart(cart: Cart, product_id: int, quantity: int, session: DB_SESSION, token: Annotated[str, Depends(validate_token)]):
    cart = add_in_cart(cart, product_id, quantity, session)
    return cart

@router.get("/view-cart", tags=["Cart"])
def view_cart(user_id : int, session: DB_SESSION):
    cart = view_of_cart(user_id, session)
    return cart

@router.delete("/delete-item-from-cart", tags=["Cart"])
def delete_from_cart(product_id: int, user_id: int, session: DB_SESSION, token: Annotated[str, Depends(validate_token)]):
    delete_item = delete_in_cart(product_id, user_id, session)
    return delete_item

@router.put('/update-cart', tags=["Cart"])
def update_cart(product_id: int, user_id: int, quantity: int, session: DB_SESSION, token: Annotated[str, Depends(validate_token)]):
    cart = update_of_cart(product_id, user_id, quantity, session)
    return cart

@router.post('/create-order', tags=["Order"])
async def create_order(session: DB_SESSION, producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)], token: Annotated[str, Depends(validate_token)]):
    order = await order_creation(token, session, producer)
    return order

@router.get('/signedin-user-orders', tags=['Order'])
def signedin_orders(session: DB_SESSION, token: Annotated[str, Depends(validate_token)]):
    orders = signedin_user_orders(session, token)
    return orders

@router.get('/user-orders', tags=['Order'])
def user_all_orders(user_id:int, session: DB_SESSION, token: Annotated[str, Depends(admin_validate_token)]):
    orders = user_orders(session, user_id)
    return orders

@router.get('/all-orders', tags=['Order'])
def orders(session: DB_SESSION, token: Annotated[str, Depends(admin_validate_token)]):
    orders = all_orders(session)
    return orders

@router.get('/all-carts', tags=['Cart'])
def list_all_carts(session: DB_SESSION, token: Annotated[str, Depends(admin_validate_token)]):
    carts = all_carts(session)
    return carts 