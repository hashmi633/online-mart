# Inventory Service - README

---

## Overview

The Inventory Service manages the inventory, suppliers, warehouses, and stock levels. It provides RESTful APIs for CRUD operations, tracks stock levels, and integrates with other microservices via Kafka for event-driven communication. The service supports seamless management of inventory and related entities, ensuring scalability and reliability.

---

## Features Implemented

### 1. Inventory Management
- **Add Inventory**: Add new inventory items.
- **View Inventory**: Retrieve all inventory items or filter by category or warehouse.
- **Update Inventory**: Modify details of existing inventory items.
- **Delete Inventory**: Remove items from inventory and update Kafka consumers.
- **Calculate Stock Levels**: Dynamically calculate available stock levels for items.

### 2. Stock Management
- **Add Stock**: Log new stock entries with batch details, supplier, and warehouse associations.
- **View Stock**: Retrieve stock entries based on item, supplier, or warehouse.
- **Deduct Stock**: Deduct stock levels when orders are processed.

### 3. Supplier Management
- **Add Supplier**: Add new suppliers with contact and address details.
- **View Suppliers**: Retrieve supplier details by ID or list all suppliers.
- **Update Supplier**: Modify supplier details.
- **Delete Supplier**: Remove supplier entries.

### 4. Warehouse Management
- **Add Warehouse**: Add new warehouses with name and location.
- **View Warehouses**: Retrieve warehouse details by ID or list all warehouses.
- **Update Warehouse**: Modify warehouse details.
- **Delete Warehouse**: Remove warehouse entries.

### 5. Kafka Integration
- **Inventory Updates**: Publishes inventory updates to the `inventory_updates` topic.
- **Inventory Deduction**: Listens to the `inventory_deduction` topic for order-related stock deductions.
- **Inventory Creation**: Consumes messages from the `inventory_creation` topic from product service to create inventory.
- **Inventory Details Response**: Sends inventory details via the `inventory_details_response` topic.

---

## Workflow

### Stock Addition Workflow
1. Validate inventory item existence.
2. Validate supplier and warehouse associations.
3. Add stock entries to inventory.
4. Publish stock updates to Kafka.

### Stock Deduction Workflow
1. Consume `inventory_deduction` messages from Kafka.
2. Deduct stock levels for specified items.
3. Publish updated stock levels to Kafka.

### Inventory Creation Workflow
1. Consume `inventory_creation` messages from Kafka.
2. Create inventory entries for new products.
3. Commit the entries to the database.

---

## Kafka Topics Used

- **inventory_updates**: Publishes stock updates for real-time synchronization.
- **inventory_deduction**: Consumes messages to deduct stock for processed orders.
- **inventory_creation**: Consumes messages to create new inventory entries.
- **inventory_details_response**: Sends inventory details to other services.

---

## Models

### Inventory Model
- **item_id**: Unique ID for the inventory item.
- **product_id**: Associated product ID.
- **product_name**: Name of the product.
- **description**: Description of the product.
- **quantity**: Current stock level.

### StockIn Model
- **stock_in_id**: Unique ID for stock entries.
- **item_id**: Reference to inventory item.
- **supplier_id**: Supplier associated with the stock entry.
- **warehouse_id**: Warehouse associated with the stock entry.
- **batch_number**: Batch details of the stock.
- **manufacture_date**: Manufacture date.
- **expiry_date**: Expiry date (if applicable).
- **cost**: Cost of the stock entry.
- **quantity**: Quantity added in the entry.

### Supplier Model
- **supplier_id**: Unique ID for the supplier.
- **supplier_name**: Name of the supplier.
- **contact**: Contact number.
- **email**: Email address.
- **address**: Physical address.

### Warehouse Model
- **warehouse_id**: Unique ID for the warehouse.
- **warehouse_name**: Name of the warehouse.
- **location**: Location of the warehouse.

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
ALGORITHM=your_algorithm
SECRET_KEY=your_secret_key
```

### 2. Install Dependencies

Install the Python packages:

```bash
pip install -r requirements.txt
``` -->

# API Endpoints

## Inventory Endpoints

- **POST** `/inventory`: Add an inventory item.
- **GET** `/inventory/{item_id}`: Retrieve details of an inventory item.
- **PUT** `/inventory/{item_id}`: Update an inventory item.
- **DELETE** `/inventory/{item_id}`: Delete an inventory item.
- **GET** `/inventory/category/{category_id}`: Retrieve inventory by category.
- **GET** `/inventory/warehouse/{warehouse_id}`: Retrieve inventory by warehouse.
- **GET** `/inventory/{item_id}/stock-level`: Calculate stock level for an item.

## Stock Endpoints

- **POST** `/stockin`: Add stock for an inventory item.
- **GET** `/stockin/{item_id}`: Retrieve stock entries by item.
- **GET** `/stockin/supplier/{supplier_id}`: Retrieve stock entries by supplier.
- **GET** `/stockin/warehouse/{warehouse_id}`: Retrieve stock entries by warehouse.

## Supplier Endpoints

- **POST** `/supplier`: Add a supplier.
- **GET** `/supplier/{supplier_id}`: Retrieve supplier details.
- **PUT** `/supplier/{supplier_id}`: Update supplier details.
- **DELETE** `/supplier/{supplier_id}`: Delete a supplier.
- **GET** `/supplier`: List all suppliers.

## Warehouse Endpoints

- **POST** `/warehouse`: Add a warehouse.
- **GET** `/warehouse/{warehouse_id}`: Retrieve warehouse details.
- **PUT** `/warehouse/{warehouse_id}`: Update warehouse details.
- **DELETE** `/warehouse/{warehouse_id}`: Delete a warehouse.
- **GET** `/get-all-warehouses`: List all warehouses.