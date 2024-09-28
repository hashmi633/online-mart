from sqlmodel import SQLModel, Field
from typing import Optional


class UserBase(SQLModel):
    user_name: str
    phone_num: Optional[int] = None

class UserAuth(SQLModel):
    user_email: str
    user_password: str

class UserModel(UserAuth, UserBase):
    pass

class User(UserModel, table=True):
    user_id: Optional[int] = Field(default=None,primary_key=True)
