from fastapi import APIRouter
from app.db.db_connector import DB_SESSION
from app.models.products import Products
from app.kafka_product import validate_inventory_item,inventory_cache


router = APIRouter()

@router.get("/")
def welcome():
    return {"Hello":"Welcome to Product Service"}


@router.post('/products', tags=["Products"])
def create_product(
        product: Products, 
        session: DB_SESSION
        ):
    validate_inventory_item(product.inventory_item_id)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

@router.get("/inventory-cache")
async def get_inventory_cache():
    return inventory_cache