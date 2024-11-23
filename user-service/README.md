# User Service

---

## Overview

The User Service handles user management, authentication, and authorization. It supports role-based access for users, Admin, and SubAdmins, providing CRUD operations for user accounts and admin functionalities. JWT-based authentication ensures secure access.

---

## Features Implemented

### 1. User Management
- **Add User**: Create a new user account.
- **Retrieve User**: Fetch user details by user ID.
- **Update User**: Modify user details.
- **Delete User**: Remove a user account.
- **List All Users**: Retrieve a list of all users.

### 2. Authentication
- **User Login**: Validate credentials and generate JWT tokens.
- **Role-Based Access**:
  - Supports Admin, SubAdmin, and User roles.
  - Separate authentication endpoints for Admin and User accounts.

### 3. Admin Management
- **Add SubAdmin**: Create SubAdmin accounts with specific privileges.
- **Fetch Admin Details**: Retrieve details of the current Admin.

### 4. JWT Security
- **Access Tokens**: Securely generate and verify tokens.
- **Password Hashing**: Encrypt passwords for secure storage.

---

## Models

### User Model
- **user_id**: Unique identifier for users.
- **user_name**: Full name of the user.
- **user_email**: Email address for authentication and notifications.
- **user_password**: Encrypted password.
- **phone_num**: Optional phone number.

### Admin Model
- **admin_id**: Unique identifier for Admin accounts.
- **admin_email**: Email address for Admin authentication.
- **admin_password**: Encrypted password.

### SubAdmin Model
- **sub_admin_id**: Unique identifier for SubAdmin accounts.
- **permissions**: Specific permissions assigned to SubAdmins.

---

## API Endpoints

### User Endpoints
- **POST** `/add_user`: Create a new user.
- **GET** `/get_user`: Retrieve a user's details by user ID.
- **PUT** `/update_user`: Update user details.
- **DELETE** `/delete_user`: Delete a user account.
- **GET** `/get-all-users`: Fetch all user accounts.

### Authentication Endpoints
- **POST** `/login`: Authenticate user or Admin and return a JWT token.
- **GET** `/get-token`: Generate and verify JWT tokens.

### Admin Endpoints
- **POST** `/add_admin`: Add SubAdmin accounts.
- **GET** `/admin`: Fetch Admin details.

---

## Workflow

### User Registration
1. User submits registration details via `/add_user`.
2. System validates email uniqueness.
3. Password is hashed and user data is saved to the database.
4. User details are published to the `users` Kafka topic.

### Authentication
1. Users or Admins log in via `/login`.
2. JWT tokens are issued based on role and stored claims.
3. Tokens are verified for secure access to protected endpoints.

### Admin Management
1. Admins can add SubAdmins via `/add_admin`.
2. Permissions are defined for SubAdmins based on system requirements.

---

<!-- ## Kafka Topics

- **users**: Publishes user data to other services.

--- -->

## Technologies Used

- **FastAPI**: Framework for building APIs.
- **SQLModel**: ORM for database interactions.
- **PostgreSQL**: Database backend.
- **JWT**: Token-based authentication.
<!-- - **Kafka**: Message broker for event-driven communication. -->

---

## How to Run

### 1. Set Environment Variables
Add the following variables to `.env`:
```env
DATABASE_URL=your_postgresql_connection_string
JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
```

<!-- ### 2. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 3. Run the Service

Start the FastAPI application:

```bash
uvicorn main:app --reload
``` -->