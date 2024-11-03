from fastapi import APIRouter, Depends
from app.db.db_connector import DB_SESSION
from app.models.products_models import ProductPrice, ProductItem, ProductCategory
from app.kafka_product import validate_inventory_item,inventory_cache, get_kafka_producer
from app.crud.product_crud import product_creation, add_to_category
from typing import Annotated
from aiokafka import AIOKafkaProducer

router = APIRouter()

@router.get("/")
def welcome():
    return {"Hello":"Welcome to Product Service"}


# @router.post('/products', tags=["Products"])
# def create_product(
#         product: Product, 
#         session: DB_SESSION
#         ):
#     validate_inventory_item(product.inventory_item_id)
#     product = create_of_product(product, session)
#     return product

# @router.post('/product-price', tags=["Products"])
# def product_price(
#         price_data: ProductPrice, 
#         session: DB_SESSION
#         ):
    
#     product_with_price = price_allocation(price_data, session)
#     return product_with_price

# @router.get('/product-name',  tags=["Products"])
# def get_product_name(id: int,
#                      session: DB_SESSION):
#     product = session.get(Product, id)
#     if product:
#         return product.prices[0].price


@router.post('/category-creation')
def category_creation(category_data: ProductCategory, session: DB_SESSION):
    category = add_to_category(category_data, session)
    return category

@router.post('/product-creation', tags=["Products"])
async def creation_of_product(
        product: ProductItem, 
        session: DB_SESSION,
        producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]
        ):
    
    product = await product_creation(product, session, producer)
    return product


@router.get("/inventory-cache")
async def get_inventory_cache():
    return inventory_cache