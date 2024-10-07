from sqlmodel import SQLModel, Field
from typing import Optional

class Category(SQLModel, table=True):
    category_id: Optional[int] = Field(default=None, primary_key=True)
    category_name: str = Field(index=True, unique=True, description="Name of the category")
    description: Optional[str] = Field(default=None,  description="Description of the category")

class Warehouse(SQLModel, table=True):
    warehouse_id: Optional[int] = Field(default=None, primary_key=True)
    warehouse_name: str = Field(index=True, unique=True,  description="Name of the warehouse")
    location: str = Field(description="Location of the warehouse")
    
class Supplier(SQLModel, table=True):
    supplier_id: Optional[int] = Field(default=None, primary_key=True)
    supplier_name: str = Field(index=True, description="Name of the supplier")
    contact: str = Field(description="Contact number of the supplier")
    email: str = Field(unique=True, index=True, description="Email address of the supplier")
    address: str = Field(description="Physical address of the supplier")

class InventoryItem(SQLModel,table=True):
    item_id : Optional[int] = Field(default=None, primary_key=True)
    category_id: int = Field(foreign_key="category.category_id", nullable=False, index=True, description="Category ID reference")
    warehouse_id: int = Field(foreign_key="warehouse.warehouse_id", nullable=False, index=True, description="Warehouse ID reference")
    supplier_id: int = Field(foreign_key="supplier.supplier_id", nullable=False, index=True, description="Supplier ID reference")
    item_name: str= Field(index=True, description="Name of the inventory item")
    cost: float = Field(description="Cost price of the item in the inventory")
    description: Optional[str] =  Field(default=None, description="Description of the item")
    weight: Optional[float] = Field(default=0.0, description="weight in kilogram") 
    batch_number: Optional[str] =Field(default=None, description="Batch number of the item")
    manufacture_date: Optional[str] = Field(default=None, description="Manufacture date of the item")
    expiry_date: Optional[str] = Field(default=None, description="Expiry date of the item, if applicable")
