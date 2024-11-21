from fastapi import APIRouter, Depends
from app.models.inventory_models import Warehouse, Supplier, Inventory, StockIn
from app.db.db_connector import DB_SESSION
from app.crud.warehouse_crud import add_to_warehouse, get_to_warehouse, update_to_warehouse, delete_to_warehouse, list_all_warehouses
from app.crud.supplier_crud import add_to_supplier, get_to_supplier, update_to_supplier, delete_to_supplier,get_all_suppliers
from app.crud.inventory_crud import add_to_inventory, get_to_inventory_item_by_id, update_to_inventory, delete_to_inventory, get_inventory_items_by_category, get_inventory_items_by_warehouse, get_all_items, update_of_inventory
from app.crud.stockin_crud import add_stock_in, get_stock_in_entries_by_item, get_stock_in_entries_by_supplier, get_stock_in_entries_by_warehouse, calculate_stock_level, calculate_item_level
from typing import Annotated
from app.shared_helper import validate_token
from app.kafka.producers.producer import get_kafka_producer
from aiokafka import AIOKafkaProducer

router = APIRouter()

@router.get('/')
def welcome():
    return{"Hello":"Welcome to Inventory Service"}

@router.post('/add_warehouse', tags=["Warehouse"])
def add_warehouse(
                warehouse_data: Warehouse,
                token: Annotated[str, Depends(validate_token)],
                session : DB_SESSION
                ):
    added_warehouse = add_to_warehouse(warehouse_data, session)
    return added_warehouse

@router.get('/warehouse/{warehouse_id}', tags=["Warehouse"])
def get_warehouse(
                warehouse_id: int,
                token: Annotated[str, Depends(validate_token)],
                session : DB_SESSION
                ):
    got_warehouse = get_to_warehouse(warehouse_id, session)
    return got_warehouse

@router.put('/update-warehouse', tags=["Warehouse"])
def update_warehouse(
                id: int,
                warehouse_data: Warehouse,
                token: Annotated[str, Depends(validate_token)],
                session : DB_SESSION
                ):
    updated_warehouse = update_to_warehouse(id,warehouse_data, session)
    return updated_warehouse

@router.delete('/delete_warehouse', tags=["Warehouse"])
def delete_warehouse(
                    id: int,
                    token: Annotated[str, Depends(validate_token)],
                    session : DB_SESSION
                    ):
    deleted_warehouse = delete_to_warehouse(id, session)
    return deleted_warehouse

@router.get('/get-all-warehouses', tags=["Warehouse"])
def get_warehouses(token: Annotated[str, Depends(validate_token)],
                    session : DB_SESSION):
    
    warehouses = list_all_warehouses(session)
    return warehouses


@router.post('/add_supplier', tags=["Supplier"])
def add_supplier(
                supplier_data: Supplier,
                token: Annotated[str, Depends(validate_token)],
                session : DB_SESSION
                ):
    added_supplier = add_to_supplier(supplier_data, session)
    return added_supplier

@router.get('/supplier/{supplier_id}', tags=["Supplier"])
def get_supplier(
                supplier_id: int,
                token: Annotated[str, Depends(validate_token)],
                session : DB_SESSION
                ):
    got_supplier = get_to_supplier(supplier_id, session)
    return got_supplier

@router.put('/update-supplier', tags=["Supplier"])
def update_supplier(
                id: int,
                supplier_data: Supplier,
                token: Annotated[str, Depends(validate_token)],
                session : DB_SESSION
                ):
    updated_supplier = update_to_supplier(id,supplier_data, session)
    return updated_supplier

@router.delete('/delete_supplier', tags=["Supplier"])
def delete_supplier(
                    id: int,
                    token: Annotated[str, Depends(validate_token)],
                    session : DB_SESSION
                    ):
    deleted_supplier = delete_to_supplier(id, session)
    return deleted_supplier

@router.get('/list-all-suppliers', tags=['Supplier'])
def list_all_suppliers(
                token: Annotated[str, Depends(validate_token)],
                session : DB_SESSION
                ):
    all_suppliers = get_all_suppliers(session)
    return all_suppliers


@router.post('/inventory', tags=['Inventory'])
def add_inventory_item(inventory_data:Inventory,
                       token: Annotated[str, Depends(validate_token)],
                       session: DB_SESSION
                       ):
    new_item = add_to_inventory(inventory_data, session)
    return new_item

@router.get('/inventory/{item_id}', tags=["Inventory"])
def get_inventory_item(
                item_id: int,
                token: Annotated[str, Depends(validate_token)],
                session : DB_SESSION
                ):
    item = get_to_inventory_item_by_id(item_id, session)
    return item

@router.put('/inventory/{item_id}', tags=["Inventory"])
def update_inventory_item(
                item_id: int,
                inventory_data: Inventory,
                token: Annotated[str, Depends(validate_token)],
                session : DB_SESSION
                ):
    updated_item = update_to_inventory(item_id,inventory_data, session)
    return updated_item

@router.delete('/inventory/{item_id}', tags=["Inventory"])
def delete_inventory(
                    item_id: int,
                    token: Annotated[str, Depends(validate_token)],
                    session : DB_SESSION,
                    producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]
                    ):
    deleted_inventory = delete_to_inventory(item_id, session)
    # await update_inventory(item_id, session, producer)
    return deleted_inventory

@router.get('/inventory/category/{category_id}', tags=['Inventory'])
def get_inventory_by_category(category_id:int,
                              token: Annotated[str, Depends(validate_token)],
                              session : DB_SESSION
                              ):
    items = get_inventory_items_by_category(category_id, session)
    return items

@router.get("/inventory/warehouse/{warehouse_id}", tags=['Inventory'])
def get_inventory_by_warehouse(warehouse_id: int,
                               token: Annotated[str, Depends(validate_token)],
                               session : DB_SESSION
                               ):
    items = get_inventory_items_by_warehouse(warehouse_id, session)
    return {"warehouse_id": warehouse_id, "items": items}

@router.get("/get-all-items", tags=["Inventory"])
def get_all_items_list(
                token: Annotated[str, Depends(validate_token)],
                session : DB_SESSION
                ):
    all_items = get_all_items(session)
    return all_items

@router.post("/stockin", tags=['StockIn'])
async def add_stock(stock_in: StockIn,
                # token: Annotated[str, Depends(validate_token)],
                session : DB_SESSION,
                producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]
                ):
    new_stock = add_stock_in(stock_in, session)
    await update_of_inventory(stock_in.item_id,session, producer)
    return {"message": "Stock added to inventory", "stock": new_stock}

@router.get("/stockin/{item_id}", tags=['StockIn'])
def get_stock_in_entries(item_id: int,
                         session : DB_SESSION
                         ):
    stock_entries = get_stock_in_entries_by_item(item_id, session)
    return {"item_id": item_id, "stock_entries": stock_entries}

@router.get("/stockin/supplier/{supplier_id}", tags=['StockIn'])
def get_stock_in_by_supplier(supplier_id: int,
                         session : DB_SESSION
                         ):
    stock_entries = get_stock_in_entries_by_supplier(supplier_id, session)
    return {"supplier_id": supplier_id, "stock_entries": stock_entries}

@router.get("/stockin/warehouse/{warehouse_id}", tags=['StockIn'])
def get_stock_in_by_warehouse(warehouse_id: int,
                         session : DB_SESSION
                         ):
    stock_entries = get_stock_in_entries_by_warehouse(warehouse_id, session)
    return {"warehouse_id": warehouse_id, "stock_entries": stock_entries}

@router.get("/inventory/{item_id}/stock-level", tags=['StockIn'])
def get_stock_level(item_id: int,
                    session : DB_SESSION
                    ):
    stock_level = calculate_stock_level(item_id, session)
    return stock_level

@router.get("/inventory/{item_id}/item-level", tags=['StockIn'])
def get_inventory_level(item_id: int,
                    session : DB_SESSION
                    ):
    inventory = calculate_item_level(item_id, session)
    return inventory
