from fastapi import APIRouter, Depends, Query
from typing import Annotated
from app.crud.crud_user import user_add,get_user_by_id,delete_user_by_id,update_user_by_id
from app.crud.crud_admin import admin_authentication
from app.db.db_connector import DB_SESSION
from app.models.user_models import UserModel, User,UserUpdate

router = APIRouter()

@router.get("/")
def welcome():
    print("Welcome to user route")
    return {"Hello":"Welcome to User Service from Base Route"}

@router.get("/get_user")
def get_user(user_id: int, session: DB_SESSION):
    user_to_get = get_user_by_id(user_id, session)
    return user_to_get

@router.post('/add_user')
def add_user(user: User, session: DB_SESSION):
    created_user = user_add(user, session)
    return created_user

@router.put('/update_user')
def update_user(user_id_to_update: int, user_update_details: UserUpdate, session: DB_SESSION):
    updated_user = update_user_by_id(user_id_to_update, user_update_details, session)
    return updated_user

@router.delete("/delete_user")
def delete_user(
    session: DB_SESSION,
    admin_email: str,
    admin_password: str,
    user_id_to_delete: int = Query(..., description="ID of the user to delete")
    ):
    admin_authenticated = admin_authentication(admin_email, admin_password, session)    
    deleted_user = delete_user_by_id(user_id_to_delete, session)
    return deleted_user

# @router.delete('/delete_user')
# def delete_user(
#     admin_context:Annotated[tuple,Depends(admin_authentication)],
#     user_id_to_delete:int = Query(..., description="ID of the user to delete")
#     ):
#     admin_user,session = admin_context
#     # user_id_to_delete = int(input("Enter User ID to delete: ")) 
#     return delete_user_by_id(user_id_to_delete,session)
