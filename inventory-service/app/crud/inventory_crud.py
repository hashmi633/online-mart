from app.models.inventory_models import Category
from sqlmodel import Session, select
from fastapi import HTTPException, Depends
from typing import Annotated
from app.jwt_helper import oauth2_scheme

def add_to_category(category_data:Category,session: Session):
    existing_category = session.exec(select(Category).where(category_data.category_id==Category.category_id)).first()
    session.add(category_data)
    session.commit()
    session.refresh(category_data)
    return category_data

