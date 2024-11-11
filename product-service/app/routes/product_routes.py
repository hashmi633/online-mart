from fastapi import APIRouter, Depends
from app.db.db_connector import DB_SESSION
from app.models.products_models import ProductPrice, ProductItem, ProductCategory
from app.kafka_product import validate_inventory_item,inventory_cache, get_kafka_producer
from app.crud.product_crud import product_creation, price_allocation, get_all_products
from app.crud.category_crud import add_to_category, get_to_category, update_to_category, delete_to_category, get_all_categories
from typing import Annotated
from aiokafka import AIOKafkaProducer

router = APIRouter()

@router.get("/")
def welcome():
    return {"Hello":"Welcome to Product Service"}

@router.post('/category-creation', tags=['Category'])
def category_creation(category_data: ProductCategory, session: DB_SESSION):
    category = add_to_category(category_data, session)
    return category

@router.get('/category/{category_id}', tags=["Category"])
def get_category(
                category_id: int,
                # token: Annotated[str, Depends(validate_token)],
                session : DB_SESSION
                ):
    got_category = get_to_category(category_id, session)
    return got_category

@router.put('/update-category', tags=["Category"])
def update_category(
                id: int,
                category_data: ProductCategory,
                # token: Annotated[str, Depends(validate_token)],
                session : DB_SESSION
                ):
    updated_category = update_to_category(category_data, session)
    return updated_category
    
@router.delete('/delete_category', tags=["Category"])
def delete_category(
                    category_id: int,
                    # token: Annotated[str, Depends(validate_token)],
                    session : DB_SESSION
                    ):
    deleted_category = delete_to_category(category_id, session)
    return deleted_category
   
@router.get('/list-all-categories', tags=['Category'])
def list_all_categories(
                # token: Annotated[str, Depends(validate_token)],
                session : DB_SESSION
                ):
    all_categories = get_all_categories(session)
    return all_categories

@router.post('/product-creation', tags=["Products"])
async def creation_of_product(
        product: ProductItem, 
        session: DB_SESSION,
        producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]
        ):
    
    product = await product_creation(product, session, producer)
    return product

@router.post('/product-price', tags=["Products"])
async def product_price(
        price_data: ProductPrice, 
        session: DB_SESSION,
        producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]
        ):
    
    product_with_price = await price_allocation(price_data, session, producer)
    return product_with_price

@router.get('/product-name',  tags=["Products"])
def get_product_name(id: int,
                     session: DB_SESSION):
    product = session.get(ProductItem, id)
    if product:
        return product.prices[0].price

@router.get('/all-products', tags=["Products"])
def all_products(session : DB_SESSION):
    products = get_all_products(session)
    return products


