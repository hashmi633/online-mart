from aiokafka import AIOKafkaConsumer
from app.email_test.smtp import to_send_email
import json


async def consume_order_notification():
    consumer = AIOKafkaConsumer(
        "order_notification",
        bootstrap_servers="broker:19092",
        group_id="notification_service_group",
        auto_offset_reset="earliest"
    )
    await consumer.start()

    try:
        async for message in consumer:
            data = json.loads(message.value.decode('utf-8'))
            order_details = data.get("order_details")
            
            order_id = order_details.get("order_id")
            order_status = order_details.get("order_status")
            email = order_details.get("user_email")
            total_amount = order_details.get("total_amount")
            user_name = order_details.get("user_name")
            print(order_id)
            print(order_status)
            print(email)
            print(total_amount)
            # Generate email subject and body
            subject = f"Order #{order_id} - {order_status.capitalize()}"
            email_template = f"""
Dear {user_name.title()},

Your order (#{order_id}) has been successfully created and is currently in "{order_status}" status.

Total Amount: ${total_amount}

Thank you for shopping with us!

Best regards,  
Khazir Mart Team
"""

            await to_send_email(email, subject,email_template)
    
    except Exception as e:
        print(f"Error consuming order notification: {e}")

    finally:
        await consumer.stop()