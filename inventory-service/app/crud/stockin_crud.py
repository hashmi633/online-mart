from app.models.inventory_models import InventoryItem, StockIn, Warehouse, Supplier
from sqlmodel import Session, select
from fastapi import HTTPException, Depends

def add_stock_in(stock_in:StockIn,session: Session):
    existing_item = session.exec(select(InventoryItem).where(stock_in.item_id==InventoryItem.item_id)).first()

    if existing_item:
        existing_supplier = session.exec(select(Supplier).where(stock_in.supplier_id==Supplier.supplier_id)).first()
        existing_warehouse = session.exec(select(Warehouse).where(stock_in.warehouse_id==Warehouse.warehouse_id)).first()
        if not existing_supplier:
             raise HTTPException(
                status_code=404,
                detail="Supplier ID does not exist."
                )         
        elif not existing_warehouse:
            raise HTTPException(
                status_code=404,
                detail="Warehouse ID does not exist."
            )
        session.add(stock_in)
        session.commit()
        session.refresh(stock_in)
        return stock_in
    
    raise HTTPException(
         status_code=404,
        detail="item id does not exist."
    )

def get_stock_in_entries_by_item(id: int, session: Session):
    item = session.exec(select(StockIn).where(id==StockIn.item_id)).all()
    if not item:
        raise HTTPException(
            status_code=404,
            detail="No stock entries found for this item"
                
        )
    return item

def get_stock_in_entries_by_supplier(id: int, session: Session):
    item = session.exec(select(StockIn).where(id==StockIn.supplier_id)).all()
    if not item:
        raise HTTPException(
            status_code=404,
            detail="No stock entries found for this supplier"
                
        )
    return item

def get_stock_in_entries_by_warehouse(id: int, session: Session):
    item = session.exec(select(StockIn).where(id==StockIn.warehouse_id)).all()
    if not item:
        raise HTTPException(
            status_code=404,
            detail="No stock entries found for this warehouse"
                
        )
    return item

def calculate_stock_level(id: int, session: Session):
    stock_entries = session.exec(select(StockIn).where(id==StockIn.item_id)).all()
    total_quantity = sum(entry.quantity for entry in stock_entries)
    return total_quantity

