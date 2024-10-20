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

