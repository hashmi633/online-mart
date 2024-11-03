from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import json
from fastapi import HTTPException

inventory_cache = {}

async def get_kafka_producer():
    producer = AIOKafkaProducer(bootstrap_servers='broker:19092')
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()

async def consume_inventory_updates():
    consumer = AIOKafkaConsumer(
        "inventory_updates",
        bootstrap_servers="broker:19092",
        group_id='product-group',
        auto_offset_reset="earliest"
    )

    await consumer.start()

    try:
        async for msg in consumer:
            data = json.loads(msg.value.decode("utf-8"))
            inventory_item_id = data['inventory_item_id']
            quantity = data['quantity']
            status = data['status']

            # Update the local cache
            inventory_cache[inventory_item_id] = {
                "quantity": quantity,
                "status": status
            }

            print(f"Updated inventory cache: {inventory_cache}")

    finally:
        await consumer.stop()

def validate_inventory_item(inventory_item_id : int):
    if inventory_item_id not in inventory_cache:
        raise HTTPException(
            status_code=400,
            detail="Inventory item does not exist."
        )
    
    item = inventory_cache[inventory_item_id]
    if item['status'] == "out_of_stock":
        raise HTTPException(
            status_code=400,
            detail="Inventory item is out of stock."
        ) 