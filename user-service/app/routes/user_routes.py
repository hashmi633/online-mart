from fastapi import APIRouter, Depends
from typing import Annotated
from app.controllers.crud_user import user_add,get_user_by_id,delete_user_by_id,update_user_by_id
from app.models.user_models import UserModel, User,UserUpdate

router = APIRouter()

@router.get("/")
def welcome():
    print("Welcome to user route")
    return {"Hello":"Welcome to User Service from Base Route"}

@router.get("/get_user")
def get_user(user: Annotated[User, Depends(get_user_by_id)]):
    return user

@router.post('/add_user')
def add_user(user: Annotated[User, Depends(user_add)]):
    return user

@router.put('/update_user')
def update_user(updated_user: Annotated[UserUpdate, Depends(update_user_by_id)]):
    return updated_user

@router.delete('/delete_user')
def delete_user(message:Annotated[str,Depends(delete_user_by_id)]):
    return message    
