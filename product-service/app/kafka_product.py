from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import json
from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.products_models import ProductItem
from app.db.db_connector import engine

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
            product_id = data["product_id"]
            inventory_item_id = data['inventory_item_id']
            quantity = data['quantity']
            status = data['status']

            # Update the local cache
            inventory_cache[product_id] = {
                "inventory_item_id" : inventory_item_id, 
                "quantity": quantity,
                "status": status
            }

            print(f"Updated inventory cache: {inventory_cache}")

    finally:
        await consumer.stop()

async def consume_products_requests():
    consumer = AIOKafkaConsumer(
        "get_product_details",
        bootstrap_servers="broker:19092",
        group_id="product-service-group",
        auto_offset_reset="earliest"
    )
    await consumer.start()
    
    producer_generator = get_kafka_producer()
    producer = await producer_generator.__anext__()  # Get the producer

    
    try:
        async for message in consumer:
            print("Received a message from Kafka")
            data = json.loads(message.value.decode("utf-8"))
            product_ids = data.get("product_ids", [])
            
            print(f"Decoded product_ids: {product_ids}")
            
            # Fetch the product details in bulk
            with Session(engine) as session:
                print("Querying the database...")
                products = session.exec(select(ProductItem).where(ProductItem.product_id.in_(product_ids))).all()
                
                print(f"Fetched products from DB: {products}")
                response_data = [
                    {
                        "product_id": product.product_id,
                        "product_name": product.product_name,
                        "price": product.prices[0].price
                    }
                    for product in products
                ]
                print(f"Response data prepared: {response_data}")
            print("Sending response to Kafka...")
            await producer.send_and_wait("products_details_response", json.dumps(response_data).encode("utf-8"))
            print(f"Message sent to products_details_response: {response_data}")
    except Exception as e:
        print(f"Error inside consumer processing: {e}")
    finally:
        print("Cleaning up producer and consumer...")
        await producer_generator.aclose()  # Ensure the producer is cleaned up
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