from app.models.products_models import  ProductPrice, ProductItem, ProductCategory
from sqlmodel import Session, select
from fastapi import HTTPException
from aiokafka import AIOKafkaProducer
import json


# def create_of_product(product : Product, session : Session):
    
#     existing_product_with_inventory_id = session.exec(select(Product).where(product.inventory_item_id==Product.inventory_item_id)).first()
#     existing_product_with_product_id = session.exec(select(Product).where(product.product_id==Product.product_id)).first()
    
#     if existing_product_with_inventory_id:
#         raise HTTPException(
#             status_code=400,
#             detail="This inventory item is already associated with a product."
#             )        
    
#     elif existing_product_with_product_id:
#         raise HTTPException(
#             status_code=400,
#             detail="This product ID already exists in the product table."
#             )
    
#     session.add(product)
#     session.commit()
#     session.refresh(product)
#     return product

# def price_allocation(price_data: ProductPrice, session: Session):
#     product_item = session.get(Product, price_data.product_id)
#     if not product_item:
#         raise HTTPException(
#             status_code=400,
#             detail="There is no product with provided id."
#         )
#     session.add(price_data)
#     session.commit()
#     session.refresh(price_data)
#     return price_data

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

def add_to_category(category_data:ProductCategory,session: Session):
    existing_category = session.exec(select(ProductCategory).where(category_data.category_id==ProductCategory.category_id)).first()
    if existing_category:
        raise HTTPException(
            status_code=400,
            detail="This category is already created"
        )
  
    session.add(category_data)
    session.commit()
    session.refresh(category_data)
    return category_data
