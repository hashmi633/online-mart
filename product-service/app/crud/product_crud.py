from app.models.products_models import  ProductPrice, ProductItem, ProductCategory
from sqlmodel import Session, select
from fastapi import HTTPException
from aiokafka import AIOKafkaProducer
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

def price_allocation(price_data: ProductPrice, session: Session):
    product_item = session.get(ProductItem, price_data.product_id)
    if not product_item:
        raise HTTPException(
            status_code=400,
            detail=f"There is no product with  id: {price_data.product_id}"
        )
    session.add(price_data)
    session.commit()
    session.refresh(price_data)
    return price_data

