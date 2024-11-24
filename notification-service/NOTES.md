Notification Send Workflow:
Order Creation:

A customer creates an order, and the Order Service processes it.
Event Publishing:

After the order is created, the Order Service publishes an event to a Kafka topic (or any other event system).
Example Code in Order Service:

python
Copy code
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=["kafka:9092"],
    value_serializer=lambda x: json.dumps(x).encode("utf-8")
)

event_payload = {
    "order_id": 12345,
    "user_id": 678,
    "order_status": "pending",
    "order_date": "2024-11-24T14:00:00Z",
    "total_amount": 150.0,
    "message": "Your order has been successfully created and is currently pending.",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."  # Optional
}

producer.send("order_notification", value=event_payload)
Notification Processing:

The Notification Service consumes the event, decodes the token (if provided), extracts the email, and uses the order details to send the notification.


Email Example
Using the event details, the Notification Service can construct and send an email like this:

Subject:
Order #12345 - Pending

Body:
vbnet
Copy code
Dear Customer,

Your order (#12345) has been successfully created on 24th November 2024 and is currently in "Pending" status.

Total Amount: $150.00

Thank you for shopping with us!

Best regards,  
Online Mart Team