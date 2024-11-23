# Notification Service - README

---

## Overview

The Notification Service is responsible for sending user notifications related to order events. Notifications include order creation, payment updates, shipping status, and delivery updates. The service is designed to listen to specific Kafka topics for event-based notifications, ensuring decoupled and scalable communication between microservices.

---

## Features Implemented

### 1. Notification on Order Creation:
- When an order is created, a notification is sent to the user to inform them that the order is in "pending" status.
- A Kafka topic (`order_notification`) is used to handle notifications asynchronously.

**Workflow:**
- After the order is created, the `order_notification` event is published by the Order Service.
- The Notification Service listens to this topic and sends an email or other forms of notifications to the user.

**Kafka Message Example:**
```json
{
    "order_id": 123,
    "user_id": 1,
    "status": "pending",
    "message": "Your order has been successfully created and is in pending status."
}
```
## Event-Based Notifications

- Notifications are triggered for key order-related events:
  - **Payment Notification**: Informs the user whether the payment was successful or failed.
  - **Shipment Notification**: Notifies the user when their order is shipped, with tracking details.
  - **Delivery Notification**: Confirms the successful delivery of the order.
- Kafka topics like `payment_notification`, `shipment_notification`, and `delivery_notification` are used for these events.

### Workflow

- The respective service (e.g., Payment, Shipment) publishes an event to the appropriate topic.
- The Notification Service consumes the event, prepares the notification, and sends it to the user.

---

## Kafka Topics Used

- **order_notification**: For notifications related to order creation.
- **payment_notification**: For notifications about payment status.
- **shipment_notification**: For updates on order shipment.
- **delivery_notification**: For delivery confirmations.

---

## Technologies Used

- **Python**: Core language for the service.
- **Kafka**: Message broker for inter-service communication.
<!-- - **SMTP/Email API**: For sending email notifications.
- **Logging**: Used for monitoring and debugging. -->

---

<!-- ## How to Run

### 1. Set Up Kafka:

- Ensure the Kafka broker is running and the required topics (`order_notification`, `payment_notification`, `shipment_notification`, `delivery_notification`) are created. -->

<!-- ### 2. Environment Variables:

- Configure the following environment variables for email notifications:
  - `SMTP_SERVER`
  - `SMTP_PORT`
  - `EMAIL_USERNAME`
  - `EMAIL_PASSWORD`

### 3. Start the Service:

- Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
- Run the Notification Service:
    ```bash
    python notification_service.py
    ``` -->

<!-- ---

## Future Enhancements

1. **Push Notifications**:
   - Integrate with a push notification service (e.g., Firebase) to send app notifications.
2. **Custom Notification Preferences**:
   - Allow users to customize notification preferences (e.g., email, SMS, push).
3. **Retry Mechanism**:
   - Implement a retry mechanism for failed notifications to ensure reliability.
4. **Logging and Monitoring**: -->
   <!-- - Integrate with centralized logging and monitoring tools (e.g., ELK Stack, Grafana) for better observability. -->