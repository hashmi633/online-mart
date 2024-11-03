from aiokafka import AIOKafkaConsumer
from sqlmodel import Session, select
from app.models.inventory_models import Inventory 

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