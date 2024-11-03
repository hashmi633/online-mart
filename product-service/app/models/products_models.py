from sqlmodel import SQLModel, Relationship, Field
from typing import Optional, List
from datetime import datetime

class ProductCategory(SQLModel, table=True):
    category_id: Optional[int] = Field(default=None, primary_key=True)
    category_name: str = Field(index=True, unique=True, description="Name of the category")
    description: Optional[str] = Field(default=None,  description="Description of the category")
    products: List["ProductItem"] = Relationship(back_populates="category")

class ProductItem(SQLModel, table=True):
    product_id: Optional[int] = Field(default=None, primary_key=True)
    product_name: str = Field(index=True, description="Name of the product item")
    category_id: int = Field(foreign_key="productcategory.category_id", nullable=False, index=True, description="Category ID reference")
    description: Optional[str] = Field(default=None, description="Description of the product")
    category : Optional["ProductCategory"] = Relationship(back_populates='products')
    prices : List["ProductPrice"] = Relationship(back_populates="product")

class ProductPrice(SQLModel, table=True):
    price_id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="productitem.product_id", nullable=False)
    price: float = Field(description="Price of the product")
    effective_date: datetime = Field(default_factory=datetime.utcnow, description="Effective date of the price")

    # Relationship back to Product
    product : "ProductItem" = Relationship(back_populates="prices")

