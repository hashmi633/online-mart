## Order Creation:
| #  | Task Description                                | Status      |
|----|------------------------------------------------|-------------|
| 1  | Retrieve the cart and associated items         | **Completed** |
| 2  | Validate product price from Product Service via Kafka | **Pending**   |
| 3  | Validate inventory levels from Inventory Service via Kafka | **Pending**   |
| 4  | Calculate the total order price                | **Completed** |
| 5  | Create an order entry in the database          | **Completed** |
| 6  | Add order items to the order                   | **Completed** |
| 7  | Deduct inventory levels from Inventory Service | **Pending**   |
| 8  | Clear the cart and associated items            | **Completed** |
| 9  | Error handling for missing or stale data       | **Pending**   |
| 10 | Add structured logging for debugging           | **Pending**   |