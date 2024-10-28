from aiokafka import AIOKafkaConsumer

async def consume_messages(topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="user-group",
        auto_offset_reset="earliest"
    )

    await consumer.start()
    try:
        async for message in consumer:
            print(f"Received message in inventory service of user add: {message.value.decode()} on topic {message.topic}")

    finally:
        await consumer.stop()