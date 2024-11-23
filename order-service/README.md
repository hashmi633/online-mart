# Order Service - README

---

## Overview

The Order Service is a microservice responsible for managing user orders, including cart operations, order creation, and integration with other services for product data and inventory management. It uses Kafka for asynchronous communication with related services, ensuring scalability and decoupling.

---

## Features Implemented

### 1. Cart Operations
- **Add to Cart**: Users can add products to their cart with specified quantities.
- **View Cart**: Users can view the contents of their cart, including total price calculations.
- **Update Cart**: Update the quantity of items in the cart.
- **Delete from Cart**: Remove a specific item from the cart.
- **View All Carts**: Retrieve all carts (for administrative purposes).

### 2. Order Management
- **Order Creation**: 
  - Validates cart contents and product availability.
  - Sends requests to the Product Service and Inventory Service via Kafka.
  - Deducts inventory levels after successful order creation.
  - Marks the order status as `pending`.

- **View Orders**: Users can retrieve all their past and current orders.

---

## Workflow

### Order Creation Flow
1. Validate the user's cart.
2. Send a request to the Product Service to fetch product details, including price and name.
3. Query the Inventory Service for product availability.
4. Create an order with validated cart data and deduct inventory.
<!-- 5. Send an event to the Notification Service to inform the user of the order's pending status. -->

---

## Kafka Topics Used

- **get_product_details**: To fetch product details from the Product Service.
- **inventory_deduction**: To deduct inventory after order creation.
<!-- - **order_notification**: To notify users of the order's status. -->

---

## Models

### Cart Model
- **cart_id**: Unique identifier for the cart.
- **user_id**: The ID of the user associated with the cart.
- **created_at**: Timestamp for when the cart was created.
- **items**: A relationship to the `CartItem` model.

### CartItem Model
- **cart_item_id**: Unique identifier for the cart item.
- **cart_id**: The ID of the cart it belongs to.
- **product_id**: The product being added to the cart.
- **product_name**: The name of the product.
- **unit_price**: Price of the product when added.
- **quantity**: Quantity of the product in the cart.

### Order Model
- **order_id**: Unique identifier for the order.
- **user_id**: The ID of the user who placed the order.
- **status**: Status of the order (`pending`, `confirmed`, etc.).
- **total_price**: Total price of the order.
- **created_at**: Timestamp for when the order was created.
- **items**: A relationship to the `OrderItem` model.

### OrderItem Model
- **order_item_id**: Unique identifier for the order item.
- **order_id**: The ID of the order it belongs to.
- **product_id**: The product in the order.
- **product_name**: The name of the product.
- **unit_price**: Price of the product at the time of the order.
- **quantity**: Quantity of the product in the order.

---

## Dependencies

### Database
- **PostgreSQL** is used as the database backend, with `SQLModel` for ORM operations.

### Kafka
- Kafka handles asynchronous messaging between services.

### APIs
- Provides RESTful endpoints using FastAPI.

---

<!-- ## How to Run

### 1. Set Up Kafka:
- Ensure that Kafka is running, and the following topics are created:
  - `get_product_details`
  - `inventory_deduction`
  <!-- - `order_notification` -->

<!-- ### 2. Configure Environment Variables:
Create a `.env` file with the following keys:
```env
DATABASE_URL=your_postgresql_connection_string
``` -->
