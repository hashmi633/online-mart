from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Warehouse(SQLModel, table=True):
    warehouse_id: Optional[int] = Field(default=None, primary_key=True)
    warehouse_name: str = Field(index=True, unique=False,  description="Name of the warehouse")
    location: str = Field(description="Location of the warehouse")
    
class Supplier(SQLModel, table=True):
    supplier_id: Optional[int] = Field(default=None, primary_key=True)
    supplier_name: str = Field(index=True, description="Name of the supplier")
    contact: str = Field(description="Contact number of the supplier")
    email: str = Field(unique=True, index=True, description="Email address of the supplier")
    address: str = Field(description="Physical address of the supplier")

class Inventory(SQLModel, table=True):
    item_id : Optional[int] = Field(default=None, primary_key=True)
    product_id : int = Field(description='ID matching the product ID')
    product_name: str
    description: str
    quantity: int = Field(default=0, description="Available quantity of the product")
    stocks: List["StockIn"] = Relationship(back_populates="inventory")

class StockIn(SQLModel, table=True):
    stock_in_id : Optional[int] = Field(default=None, primary_key=True)
    item_id: int = Field(foreign_key="inventory.item_id", nullable=False, description="Inventory Item reference")  
    supplier_id: int = Field(foreign_key="supplier.supplier_id", nullable=False, index=True, description="Supplier ID reference")
    warehouse_id: int = Field(foreign_key="warehouse.warehouse_id", nullable=False, index=True, description="Warehouse ID reference")
    batch_number: Optional[str] = Field(default=None, description="Batch number of the item")
    manufacture_date: Optional[str] = Field(default=None, description="Manufacture date of the item")
    expiry_date: Optional[str] = Field(default=None, description="Expiry date of the item, if applicable")
    cost: float = Field(description="Cost price of the item in the stock entry")
    quantity: int = Field(default=0, description="Quantity added to stock")
    stock_in_date: Optional[str] = Field(default=None, description="Date the stock was added")
    inventory : "Inventory" = Relationship(back_populates="stocks")