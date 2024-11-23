# Online Mart API

---

## Overview

The **Online Mart API** is a modular and scalable e-commerce platform designed with microservices architecture. Each service is responsible for a specific domain, such as user management, order processing, product inventory, payment handling, and notifications. These microservices communicate asynchronously via Kafka to ensure decoupled and efficient workflows.

---

## Microservices Overview

### 1. **User Service**
Manages user accounts, authentication, and role-based access control.

- **Features**:
  - User registration and management.
  - Role-based authentication (Admin, SubAdmin, User).
  - JWT-secured endpoints.
- **Technology Stack**:
  - FastAPI, SQLModel, PostgreSQL, Kafka.

<!-- [Read the User Service README](./user_service/README.md) -->

---

### 2. **Order Service**
Handles order creation, management, and status updates.

- **Features**:
  - Order CRUD operations.
  - Integration with Product, Inventory, and Payment services.
  - Kafka-powered event-driven workflows.
- **Technology Stack**:
  - FastAPI, SQLModel, PostgreSQL, Kafka.

<!-- [Read the Order Service README](./order_service/README.md) -->

---

### 3. **Product Service**
Manages product categories, product details, and pricing.

- **Features**:
  - CRUD operations for products and categories.
  - Dynamic pricing allocation.
  - Kafka-based data sharing.
- **Technology Stack**:
  - FastAPI, SQLModel, PostgreSQL, Kafka.

<!-- [Read the Product Service README](./product_service/README.md) -->

---

### 4. **Inventory Service**
Tracks inventory levels, warehouse data, and supplier details.

- **Features**:
  - Stock management.
  - Integration with Product and Order services.
  - Kafka-powered inventory updates.
- **Technology Stack**:
  - FastAPI, SQLModel, PostgreSQL, Kafka.

<!-- [Read the Inventory Service README](./inventory_service/README.md) -->

---

<!-- ### 5. **Payment Service**
Handles payment processing, verification, and refunds.

- **Features**:
  - Payment initiation and verification.
  - Refund handling and updates.
  - Secure and tokenized payment processing.
- **Technology Stack**:
  - FastAPI, Kafka, SQLModel, Third-Party Payment Gateway APIs.

[Read the Payment Service README](./payment_service/README.md)

--- -->

### 6. **Notification Service**
Sends user notifications related to order events, payment status, and shipping updates.

- **Features**:
  - Order, payment, and shipping notifications.
  - Kafka-based event-driven notifications.
  <!-- - Email integration via SMTP or APIs. -->
- **Technology Stack**:
  - FastAPI, Kafka
  <!-- , SMTP. -->

<!-- [Read the Notification Service README](./notification_service/README.md) -->

---

## Architecture

### Communication
1. **User Interaction**:
   - Users interact via REST APIs, secured with JWT tokens.

2. **Inter-Service Communication**:
   - Kafka topics are used for event-driven workflows and data synchronization.

<!-- 3. **Data Isolation**:
   - Each microservice maintains its own database, ensuring modularity. -->

### High-Level Design
- **Frontend**: Communicates with the backend via REST APIs.
- **Backend**: Microservices communicate asynchronously using Kafka.
- **Database**: PostgreSQL is used as the primary database for all services.

---

## Kafka Topics

### Key Topics Used:
- `order_notification`: Notifications related to order events.
- `inventory_deduction`: Updates for inventory stock levels.
- `payment_status`: Payment success or failure updates.
- `shipment_notification`: Updates on order shipment.
- `users`: User data synchronization.

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
    - **Order Service**: `http://localhost:8002`
    - **Product Service**: `http://localhost:8003`
    - **Inventory Service**: `http://localhost:8004`
    <!-- - **Payment Service**: `http://localhost:8005`
    - **Notification Service**: `http://localhost:8006` -->

---

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
4. Provide a detailed description of your changes.
