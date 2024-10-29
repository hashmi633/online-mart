from sqlmodel import SQLModel, Relationship, Field
from typing import Optional

class Products(SQLModel, table=True):
    product_id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, description="Name of the product")
    description: Optional[str] = Field(default=None, description="Product description")
    price: float = Field(description="Price of the product")
    inventory_item_id: int = Field(nullable=False, description="Reference to Inventory Item ID")
    