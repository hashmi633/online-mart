from app.models.inventory_models import Supplier
from sqlmodel import Session, select
from fastapi import HTTPException, Depends



def add_to_supplier(supplier_data:Supplier,session: Session):
    existing_supplier = session.exec(select(Supplier).where(supplier_data.supplier_id==Supplier.supplier_id)).first()
    if not existing_supplier:
        session.add(supplier_data)
        session.commit()
        session.refresh(supplier_data)
        return supplier_data
    raise HTTPException(
         status_code=404,
        detail="supplier already exists with provided id."
    )

def get_to_supplier(id:int,session: Session):
    find_supplier = session.exec(select(Supplier).where(id==Supplier.supplier_id)).first()
    if find_supplier:
        return find_supplier
    raise HTTPException(
        status_code=404,
        detail="no supplier exits with this id"
    )

def update_to_supplier(id:int, supplier_data: Supplier, session: Session):
    find_supplier = session.exec(select(Supplier).where(id==Supplier.supplier_id)).first()
    if find_supplier:
        if supplier_data.supplier_name is not None:
            find_supplier.supplier_name = supplier_data.supplier_name
        if supplier_data.contact is not None:
            find_supplier.contact = supplier_data.contact
        if supplier_data.email is not None:
            find_supplier.email = supplier_data.email
        if supplier_data.address is not None:
            find_supplier.address = supplier_data.address      

        session.add(find_supplier)
        session.commit()
        session.refresh(find_supplier)
        return find_supplier
    
    raise HTTPException(
        status_code=404,
        detail="No supplier exist with this id"
    )


def delete_to_supplier(id:int,
                    session: Session):
    to_delete_supplier = session.exec(select(Supplier).where(id==Supplier.supplier_id)).first()
    if not to_delete_supplier:
        raise HTTPException(
            status_code=404,
            detail="no supplier exists with this id",
        )
    to_delete_supplier_name = to_delete_supplier.supplier_name
    to_delete_supplier_contact = to_delete_supplier.contact
    to_delete_supplier_address = to_delete_supplier.address
    session.delete(to_delete_supplier)
    session.commit()
    return f"Supplier with id: '{id}', name: '{to_delete_supplier_name}', contact: '{to_delete_supplier_contact}' and address: '{to_delete_supplier_address}' has been deleted."

def get_all_suppliers(session: Session):
    all_suppliers = session.exec(select(Supplier)).all()
    if not all_suppliers:
        raise HTTPException(
            status_code=404,
            detail="No category exist.",
        )
    return all_suppliers
