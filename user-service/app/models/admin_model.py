from sqlmodel import SQLModel,Field
from typing import Optional

class Admin(SQLModel,table=True):
    admin_id : Optional[int] = Field(default=None,primary_key=True)
    admin_email: str = Field(index=True, unique=True)
    admin_password:str
