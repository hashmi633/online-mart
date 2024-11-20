from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import json

inventory_cache = {}
product_cache = {}

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
        group_id='order-group',
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

async def consume_product_updates():
    consumer = AIOKafkaConsumer(
        "product_data",
        bootstrap_servers="broker:19092",
        group_id='product-order-group',
        auto_offset_reset="earliest"
    )

    await consumer.start()

    try:
        async for msg in consumer:
            data = json.loads(msg.value.decode("utf-8"))
            product_id = data['product_id']
            product_name = data['product_name']
            price = data['price']

            # Update the product cache
            product_cache[product_id] = {
                "product_name": product_name,
                "price": price
            }

            print(f"Updated product cache: {product_cache[product_id]}")

    finally:
        await consumer.stop()

async def consume_product_responses():
    consumer = AIOKafkaConsumer(
        "products_details_response",
        bootstrap_servers='broker:19092',
        group_id="order-service-group",
        auto_offset_reset="earliest"
    )
    await consumer.start()
    try:
        async for message in consumer:
            products_data = json.loads(message.value.decode("utf-8"))
            print(f'Received product details: {products_data}')
            return products_data
    finally:
        await consumer.stop()

async def consume_product_quantity_responses():
    consumer = AIOKafkaConsumer(
        "inventory_details_response",
        bootstrap_servers='broker:19092',
        group_id="order-product-quantity-group",
        auto_offset_reset="earliest"
    )
    await consumer.start()
    try:
        async for message in consumer:
            products_data = json.loads(message.value.decode("utf-8"))
            print(f'Received product details: {products_data}')
            return products_data
    finally:
        await consumer.stop()