from app.models.products_models import  ProductPrice, ProductItem
from sqlmodel import Session, select
from fastapi import HTTPException
from aiokafka import AIOKafkaProducer
from typing import List
import json


async def product_creation(product: ProductItem, session: Session, producer: AIOKafkaProducer):
    existing_product = session.get(ProductItem, product.product_id)
    if existing_product:
        raise HTTPException(
            status_code=400,
            detail="This product is already created."
        )
    
    session.add(product)
    session.commit()
    session.refresh(product)
    
    product_to_inventory = {
        "product_id": product.product_id,
        "product_name": product.product_name,
        "description": product.description
    }

    product_to_inventory_json = json.dumps(product_to_inventory).encode('utf-8')
    await producer.send_and_wait("inventory_creation", product_to_inventory_json)

    return product

async def price_allocation(price_data: ProductPrice, session: Session, producer: AIOKafkaProducer):
    product_item = session.get(ProductItem, price_data.product_id)
    if not product_item:
        raise HTTPException(
            status_code=400,
            detail=f"There is no product with  id: {price_data.product_id}"
        )
    session.add(price_data)
    session.commit()
    session.refresh(price_data)
    
    product_to_others = {
         "product_id": price_data.product_id,
        "product_name": price_data.product.product_name,
        "price": price_data.price
    }

    product_to_others_json = json.dumps(product_to_others).encode("utf-8")
    await producer.send_and_wait("product_data", product_to_others_json)
    
    return price_data

def get_all_products(session : Session)-> List[ProductItem]:
    all_products = session.exec(select(ProductItem)).all()
    return all_products
