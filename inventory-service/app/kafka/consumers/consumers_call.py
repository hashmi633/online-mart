import asyncio
from app.db.db_connector import DB_SESSION
from app.kafka.consumers.inventory_consumer import consume_inventory_creation, consume_inventory_requests
from sqlmodel import Session
from app.db.db_connector import engine

def consumer_call():
    with Session(engine) as session:
        asyncio.create_task(consume_inventory_creation("inventory_creation", 'broker:19092', session))
        asyncio.create_task(consume_inventory_requests())
        return {"Inventory Created and Quantity Confirmed"}    

