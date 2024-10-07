from app.models.inventory_models import Category
from sqlmodel import Session, select

def add_to_category(category_data:Category,session: Session):
    existing_category = session.exec(select(Category).where(category_data.category_id==Category.category_id)).first()
    session.add(category_data)
    session.commit()
    session.refresh(category_data)
    return category_data