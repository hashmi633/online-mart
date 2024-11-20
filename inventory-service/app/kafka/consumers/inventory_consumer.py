from aiokafka import AIOKafkaConsumer
from sqlmodel import Session, select
from app.models.inventory_models import Inventory 
from app.db.db_connector import engine
from app.crud.stockin_crud import calculate_stock_level

import json

async def consume_inventory_creation(topic, bootstrap_servers, session: Session):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id='inventory_group',
        auto_offset_reset='earliest'
    )

    await consumer.start()

    try:
        async for msg in consumer:
            data = json.loads(msg.value.decode('utf-8'))
            product_id  = data['product_id']
            existing_inventory = session.get(Inventory, data['product_id'] )
            if existing_inventory:
                print(f"Inventory entry for product_id {data['product_id']} already exists.")
                continue
            
            new_inventory = Inventory(
                product_id = data['product_id'],
                product_name = data['product_name'],
                description= data['description']
            )
            print(f"line 2: Adding new inventory entry named {data['product_name']}")

            session.add(new_inventory)
            session.commit()
            session.refresh(new_inventory)
            print(f"Created inventory entry for product_id {data['product_id']}.")

    finally:
        await consumer.stop()

async def consumer_inventory_requests():
    consumer = AIOKafkaConsumer(
        "get_product_details",
        bootstrap_servers="broker:19092",
        group_id="inventory-service-group",
        auto_offset_reset="earliest"
    )
    await consumer.start()

    try:
        async for message in consumer:
            data = json.loads(message.value.decode('utf-8'))
            product_ids = data.get("product_ids", [])
            with Session(engine) as session:
                products = session.exec(select(Inventory).where(Inventory.product_id.in_(product_ids))).all()
                response_data = [
                    {
                        "product_id": product.product_id,
                        "quantity": product.quantity
                    }
                    for product in products
                ]    

    finally:
        consumer.stop()