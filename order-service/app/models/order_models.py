from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class Cart(SQLModel, table=True):
    cart_id : Optional[int] = Field(default=None, primary_key=True)
    user_id : int = Field(index=True, description="ID of the user who owns the cart")
    created_at : datetime = Field(default_factory=datetime.utcnow, description="Time when the cart was created")
    
    # Relationship to CartItems
    items : List["CartItem"] = Relationship(back_populates="cart")

class CartItem(SQLModel, table=True):
    cart_item_id : Optional[int] = Field(default=None, primary_key=True)
    cart_id : int = Field(foreign_key="cart.cart_id", description="Foreign key referencing the cart")
    product_id : int = Field(description="ID of the product")
    product_name : str = Field(description="Name of the product from Product Service")
    unit_price : float = Field(description="Price of the product at the time of adding to cart")
    quantity : int = Field(description="Quantity of the product added to the cart")
    
    # Relationship to Cart
    cart : Cart = Relationship(back_populates="items")

class Order(SQLModel, table=True):
    order_id : Optional[int] = Field(default=None, primary_key=True)
    user_id : int = Field(index=True, description="ID of the user who placed the order")
    status : str = Field(default="pending", description="Order status (e.g., pending, confirmed, shipped, delivered)")
    total_price : float = Field(description="Total price of the order")
    created_at : datetime = Field(default_factory=datetime.utcnow, description="Time when the order was created")

    # Relationship to OrderItems
    items : List["OrderItem"] = Relationship(back_populates="order")

class OrderItem(SQLModel, table=True):
    order_item_id : Optional[int] = Field(default=None, primary_key=True)
    order_id : int = Field(foreign_key="order.order_id", description="Foreign key referencing the order")
    product_id : int = Field(description="ID of the product")
    product_name : str = Field(description="Name of the product from Product Service")
    unit_price : float = Field(description="Final price of the product at the time of order")
    quantity : int = Field(description="Quantity of the product in the order")

    # Relationship to Order
    order : Order = Relationship(back_populates="items") 