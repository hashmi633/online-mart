from fastapi import APIRouter, Depends
from app.models.inventory_models import Category,Warehouse,InventoryItem
from app.db.db_connector import DB_SESSION, get_session
from app.crud.inventory_crud import add_to_category
from typing import Annotated
from sqlmodel import Session

router = APIRouter()

@router.get('/')
def welcome():
    return{"Hello":"Welcome to Inventory Service"}

@router.post('/add_category')
def add_category(category_details: Category, session:DB_SESSION):
    # print("Received category:", category_details)
    added_category = add_to_category(category_details,session)
    return added_category