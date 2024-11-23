# Product Service - README

---

## Overview

The Product Service manages product categories, products, and pricing. It supports CRUD operations for product categories and products, handles price allocation, and communicates with other microservices via Kafka for event-driven workflows. The service ensures seamless product management and integration within the overall system.

---

## Features Implemented

### 1. Category Management
- **Create Category**: Add new product categories.
- **Update Category**: Modify existing category details.
- **Delete Category**: Remove categories from the database.
- **Get Category**: Retrieve category details by ID.
- **List All Categories**: Fetch a list of all product categories.

### 2. Product Management
- **Create Product**: Add new products and associate them with categories.
- **Update Product**: Modify product details such as name or description.
- **Delete Product**: Remove a product from the database.
- **List All Products**: Fetch details of all products.
- **Assign Price**: Allocate or update product pricing with effective dates.

### 3. Kafka Integration
- **Inventory Creation**: Sends product details to the `inventory_creation` topic upon product creation.
- **Product Data Sharing**: Publishes product data, including name and price, to the `product_data` topic for consumption by other services.
- **Product Detail Response**: Responds to requests from other services with product details via the `products_details_response` topic.

---

## Workflow

### Product Creation Workflow
1. Accept product details via the `POST /product-creation` endpoint.
2. Validate product uniqueness.
3. Persist product in the database.
4. Send product details to the `inventory_creation` Kafka topic.

### Price Allocation Workflow
1. Accept price data via the `POST /product-price` endpoint.
2. Validate product existence.
3. Store price details with effective dates in the database.
4. Publish price and product details to the `product_data` Kafka topic.

---

## Kafka Topics Used

- **inventory_creation**: Sends product details for inventory creation.
- **product_data**: Publishes product data including pricing for other services.
- **products_details_response**: Responds with product details for inter-service communication.

---

## Models

### ProductCategory Model
- **category_id**: Unique ID for the category.
- **category_name**: Name of the category.
- **description**: Optional description of the category.
- **products**: List of associated products.

### ProductItem Model
- **product_id**: Unique ID for the product.
- **product_name**: Name of the product.
- **category_id**: Reference to the category.
- **description**: Optional description of the product.

### ProductPrice Model
- **price_id**: Unique ID for the price entry.
- **product_id**: Reference to the product.
- **price**: Price value.
- **effective_date**: Date when the price becomes active.

---

## Dependencies

- **FastAPI**: Framework for building APIs.
- **SQLModel**: ORM for database interactions.
- **Kafka**: Message broker for inter-service communication.
- **PostgreSQL**: Database backend.

---

<!-- ## How to Run

### 1. Configure Environment Variables
Add the following variables to the `.env` file:
```env
DATABASE_URL=your_postgresql_connection_string
```
### 2. Install Dependencies

Install the Python packages:

```bash
pip install -r requirements.txt
```

### 3. Run the Service

Start the FastAPI server:

```bash
uvicorn main:app --reload
``` -->

## API Endpoints

### Category Endpoints

- **POST** `/category-creation`: Add a new category.
- **GET** `/category/{category_id}`: Get category details by ID.
- **PUT** `/update-category`: Update an existing category.
- **DELETE** `/delete_category`: Delete a category.
- **GET** `/list-all-categories`: List all categories.

### Product Endpoints

- **POST** `/product-creation`: Create a new product.
- **POST** `/product-price`: Assign a price to a product.
- **GET** `/product-name`: Get product name by ID.
- **GET** `/all-products`: List all products.