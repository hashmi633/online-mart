from app.models.inventory_models import Inventory, StockIn, Warehouse
from app.crud.stockin_crud import calculate_stock_level
from sqlmodel import Session, select
from fastapi import HTTPException, Depends
from app.kafka.producers.producer import get_kafka_producer
from aiokafka import AIOKafkaProducer
from typing import Annotated
import json

def add_to_inventory(inventory_data:Inventory,session: Session):
    existing_inventory = session.exec(select(Inventory).where(inventory_data.item_id==Inventory.item_id)).first()
    if not existing_inventory:
        session.add(inventory_data)
        session.commit()
        session.refresh(inventory_data)
        return inventory_data
    raise HTTPException(
         status_code=404,
        detail="inventory already exists with provided id."
    )

def get_to_inventory_item_by_id(id:int,session: Session):
    find_inventory = session.exec(select(Inventory).where(id==Inventory.item_id)).first()
    if find_inventory:
        return find_inventory
    raise HTTPException(
        status_code=404,
        detail="no inventory exits with this id"
    )

def update_to_inventory(id:int, inventory_data: Inventory, session: Session):
    find_inventory = session.exec(select(Inventory).where(id==Inventory.item_id)).first()
    if find_inventory:
        if inventory_data.item_name is not None:
            find_inventory.item_name = inventory_data.item_name
        if inventory_data.category_id is not None:
            find_inventory.category_id = inventory_data.category_id
        if inventory_data.description is not None:
            find_inventory.description = inventory_data.description
        
        session.add(find_inventory)
        session.commit()
        session.refresh(find_inventory)
        return find_inventory
    
    raise HTTPException(
        status_code=404,
        detail="no item exist with this id"
    )

def delete_to_inventory(id:int,
                    session: Session):
    to_delete_inventory = session.exec(select(Inventory).where(id==Inventory.item_id)).first()
    if not to_delete_inventory:
        raise HTTPException(
            status_code=404,
            detail="no item exists with this id",
        )
    to_delete_item_name = to_delete_inventory.item_name
    to_delete_inventory_category = to_delete_inventory.category_id
    
    session.delete(to_delete_inventory)
    session.commit()
    return f"InventoryItem with id: '{id}', name: '{to_delete_item_name}', category: '{to_delete_inventory_category}' has been deleted."

def get_inventory_items_by_category(category_id: int, session: Session):
    items = session.exec(select(Inventory).where(category_id==Inventory.category_id)).all()
    
    if not items:
        raise HTTPException(
            status_code=404,
            detail=f"No inventory items found for category id {category_id}"
        )
    
    return items

def get_inventory_items_by_warehouse(warehouse_id : int, session : Session):
    check_warehouse = session.exec(select(Warehouse).where(warehouse_id==Warehouse.warehouse_id)).first()
    if check_warehouse: 
        items = session.exec(select(StockIn).where(warehouse_id==StockIn.warehouse_id)).all()

        if not items:
            raise HTTPException(
                status_code=404,
                detail=f"No inventory items found for warehouse id {warehouse_id}"
            )
        
        return items

    raise HTTPException(
                status_code=404,
                detail=f"No warehouse exits id {warehouse_id}"
    )

def get_all_items(session: Session):
    items = session.exec(select(Inventory)).all()
    if not items:
        raise HTTPException(
            status_code=404,
            detail=f"No inventory item is added yet"
        )
    return items

async def update_of_inventory(
         item_id: int,
         session: Session,
         producer: AIOKafkaProducer
        ):
    inventory_item = session.get(Inventory, item_id)
    if not inventory_item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
     # Use calculate_stock_level to get the total quantity
    total_quantity = calculate_stock_level(item_id, session)

    # Determine status based on quantity
    status = "available" if total_quantity > 0 else "out_of_stock"

    # Prepare the Kafka message
    inventory_updates = {
        "inventory_item_id": item_id,  # Corresponds to item_id in InventoryItem table
        "quantity": total_quantity,
        "status": status
    }

    inventory_json = json.dumps(inventory_updates).encode("utf-8")

    # Send the message to Kafka topic "inventory_updates"
    await producer.send_and_wait("inventory_updates", inventory_json)
    return {"message": "Inventory updated and event sent to Kafka"}
