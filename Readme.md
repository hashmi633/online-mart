# Online Mart API

---

## Overview

The **Online Mart API** is a modular and scalable e-commerce platform designed with microservices architecture. Each service is responsible for a specific domain, such as user management, order processing, product inventory, payment handling, and notifications. These microservices communicate asynchronously via Kafka to ensure decoupled and efficient workflows.

---

## Microservices Overview

1. **User Service**: Handles user registration, authentication, and role-based access control.
2. **Product Service**: Manages product categories, product details, and pricing.
3. **Order Service**: Processes user orders, manages cart operations, and integrates with inventory and product services.
4. **Inventory Service**: Tracks inventory levels, handles stock management, and interacts with orders for availability checks.
5. **Notification Service**: Sends email notifications for critical user events like order creation, payment confirmation, and shipment updates.
6. **Payment Service**: Processes user payments and updates order statuses accordingly.
---
## Workflow

### 1. User Creation (`POST /add_user` - User Service)  
Registers new users.

### 2. Adding Warehouse (`POST /add_warehouse` - Inventory Service)  
Adds a new warehouse to the inventory system and saves it to the database. **Requires admin authentication**.

### 3. Adding Supplier (`POST /add_supplier` - Inventory Service)  
Registers supplier details for procurement and tracking purposes. **Requires admin authentication**.

### 4. Adding Category (`POST /category-creation` - Product Service)  
Creates a new product category and saves it for future product association.

### 5. Define Product (`POST /product-creation` - Product Service)  
Registers product details, stores them, and publishes the `inventory_creation` topic to initialize inventory in the Inventory Service.

### 6. Define Product Price (`POST /product-price` - Product Service)  
Sets or updates product prices and publishes the `product_data` topic for the Order Service.

### 7. Adding Stock in Inventory (`POST /stockin` - Inventory Service)  
Updates inventory stock levels and publishes the `inventory_updates` topic for the Order Service.

### 8. Add to Cart (`POST /add-to-cart` - Order Service)  
Allows users to add products to their cart for future order creation. inventory availability and product price used from cache.

### 9. Order Creation (`POST /order` - Order Service)  

Processes user orders, validates product availability, and deducts stock using Kafka topics:
- **Price Validation**: Sends product details request to Product Service (`get_product_details` topic). Product Service responds to Order Service with the topic `products_details_response`.
- **Availability Check**: Sends product details request to Inventory Service (`get_product_details` topic). Inventory Service responds to Order Service with the topic `inventory_details_response`.
- **Inventory Deduction**: Publishes a deduction request to Inventory Service (`inventory_deduction` topic).
- **Notification**: Publishes order details to Notification Service (`order_notification` topic).

### 10. Notifications (`Kafka Topics`)  
Notifies users of order creation and subsequent events via Kafka topics:
- **Order Notifications**: `order_notification`  
<!-- - **Payment Notifications**: `payment_notification`  
- **Shipment Notifications**: `shipment_notification`  
- **Delivery Notifications**: `delivery_notification`   -->
---
## Kafka Topics

| Topic Name               | Purpose                                                      |
|--------------------------|-------------------------------------------------------------|
| `inventory_creation`    | Triggers inventory creation for products.             |
| `product_data`          | Shares product price and details with the Order Service and stores it in cache.    |
| `inventory_data`        | Shares inventory stock levels with the Order Service and stores it in cache.        |
| `get_product_details`   | Used by Order Service at order creation to request product and inventory details. |
| `products_details_response` | Responds to `get_product_details` for product details from Product Service. |
| `inventory_details_response` | Responds to `get_product_details` for inventory details from Inventory Service. |
| `inventory_deduction`   | Deducts stock levels for processed orders.                  |
| `order_notification`    | Notifies users of order creation or updates.                |
<!-- | `payment_notification`  | Notifies users of payment statuses.                         |
| `shipment_notification` | Notifies users of shipping updates.                         |
| `delivery_notification` | Confirms successful order delivery.                         | -->
---

## Environment Setup

### Prerequisites
1. Install Docker and Docker Compose.
2. Ensure Kafka broker is running.
3. Set up PostgreSQL databases for each service.

<!-- ### Clone the Repository
```bash
git clone https://github.com/your-repo/online-mart-api.git
cd online-mart-api
``` -->

## Deployment

### Using Docker Compose

1. Build and start all services:

    ```bash
    docker-compose up --build
    ```

2. Access the APIs:
    - **User Service**: `http://localhost:8081`
    - **Inventory Service**: `http://localhost:8002`
    - **Product Service**: `http://localhost:8003`
    - **Order Service**: `http://localhost:8004`   
    <!-- - **Payment Service**: `http://localhost:8005` -->
    - **Notification Service**: `http://localhost:8005`

<!-- ---

## Future Enhancements

1. **Centralized Logging and Monitoring**:
    - Use tools like ELK Stack or Grafana for observability.
2. **Push Notifications**:
    - Add mobile and web push notification capabilities.
3. **Role Customization**:
    - Allow dynamic role creation with granular permissions.
4. **Analytics Dashboard**:
    - Provide an analytics dashboard for business insights.
5. **Scalability**:
    - Migrate to Kubernetes for scaling.

---

## Contribution Guidelines

1. Fork the repository.
2. Create a feature branch for your changes.
3. Test thoroughly before submitting a pull request.
4. Provide a detailed description of your changes. -->
