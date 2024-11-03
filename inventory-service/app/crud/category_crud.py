from app.models.inventory_models import Category
from sqlmodel import Session, select
from fastapi import HTTPException, Depends

def add_to_category(category_data:Category,session: Session):
    existing_category = session.exec(select(Category).where(category_data.category_id==Category.category_id)).first()
    session.add(category_data)
    session.commit()
    session.refresh(category_data)
    return category_data

def get_to_category(category_id:int,session: Session):
    find_category = session.exec(select(Category).where(category_id==Category.category_id)).first()
    if find_category:
        return find_category
    raise HTTPException(
        status_code=404,
        detail="no category exits with this id"
    )

def update_to_category(category_id:int, category_data: Category, session: Session):
    find_category = session.exec(select(Category).where(category_id==Category.category_id)).first()
    if find_category:
        if category_data.category_name is not None:
            find_category.category_name = category_data.category_name
        if category_data.description is not None:
            find_category.description = category_data.description

        session.add(find_category)
        session.commit()
        session.refresh(find_category)

        return find_category
    raise HTTPException(
        status_code=404,
        detail="No Category exist with this id"
    )

def delete_to_category(category_id:int,
                    session: Session):
    to_delete_category = session.exec(select(Category).where(category_id==Category.category_id)).first()
    if not to_delete_category:
        raise HTTPException(
            status_code=404,
            detail="No Category exist with this id",
        )
    to_delete_category_name = to_delete_category.category_name
    session.delete(to_delete_category)
    session.commit()
    return f"Category with id: {category_id} and name: '{to_delete_category_name}' has been deleted."

def get_all_categories(session: Session):
    all_categories = session.exec(select(Category)).all()
    if not all_categories:
        raise HTTPException(
            status_code=404,
            detail="No category exist.",
        )
    return all_categories

