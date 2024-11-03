from app.models.inventory_models import Warehouse
from sqlmodel import Session, select
from fastapi import HTTPException, Depends

def add_to_warehouse(warehouse_data:Warehouse,session: Session):
    existing_warehouse = session.exec(select(Warehouse).where(warehouse_data.warehouse_id==Warehouse.warehouse_id)).first()
    if not existing_warehouse:
        session.add(warehouse_data)
        session.commit()
        session.refresh(warehouse_data)
        return warehouse_data
    raise HTTPException(
         status_code=404,
        detail="warehouse already exists with provided id."
    )

def get_to_warehouse(warehouse_id:int,session: Session):
    find_warehouse = session.exec(select(Warehouse).where(warehouse_id==Warehouse.warehouse_id)).first()
    if find_warehouse:
        return find_warehouse
    raise HTTPException(
        status_code=404,
        detail="no warehouse exits with this id"
    )

def update_to_warehouse(id:int, warehouse_data: Warehouse, session: Session):
    find_warehouse = session.exec(select(Warehouse).where(id==Warehouse.warehouse_id)).first()
    if find_warehouse:
        if warehouse_data.warehouse_name is not None:
            find_warehouse.warehouse_name = warehouse_data.warehouse_name
        if warehouse_data.location is not None:
            find_warehouse.location = warehouse_data.location

        session.add(find_warehouse)
        session.commit()
        session.refresh(find_warehouse)

        return find_warehouse
    raise HTTPException(
        status_code=404,
        detail="No warehouse exist with this id"
    )

def delete_to_warehouse(id:int,
                    session: Session):
    to_delete_warehouse = session.exec(select(Warehouse).where(id==Warehouse.warehouse_id)).first()
    if not to_delete_warehouse:
        raise HTTPException(
            status_code=404,
            detail="No Warehouse exist with this id",
        )
    to_delete_warehouse_name = to_delete_warehouse.warehouse_name
    to_delete_warehouse_location = to_delete_warehouse.location
    session.delete(to_delete_warehouse)
    session.commit()
    return f"Warehouse with id: '{id}', name: '{to_delete_warehouse_name}' and location: '{to_delete_warehouse_location}' has been deleted."

def list_all_warehouses(session: Session):
    warehouses = session.exec(select(Warehouse)).all()
    return warehouses
