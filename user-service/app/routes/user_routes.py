from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Annotated
from app.crud.crud_user import user_add,get_user_by_id,delete_user_by_id,update_user_by_id, fetch_all_users , get_current_user, admin_or_user
from app.crud.crud_admin import admin_authentication, get_current_admin, pwd_context, sub_admin
from app.db.db_connector import DB_SESSION
from app.models.user_models import UserModel, User,UserUpdate
from app.models.admin_model import Admin, SubAdmin
from fastapi.security import OAuth2PasswordRequestForm
from app.helpers.jwt_helper import oath2_scheme, create_access_token, verify_token
from sqlmodel import select

router = APIRouter()

@router.get("/")
def welcome():
    print("Welcome to user route")
    return {"Hello":"Welcome to User Service from Base Route"}

@router.get("/get_user")
def get_user(user_id: int, session: DB_SESSION, token: str = Depends(oath2_scheme)):
    user_to_get = get_user_by_id(user_id, session)
    return user_to_get

@router.post('/add_user')
def add_user(user: User, session: DB_SESSION):
    created_user = user_add(user, session)
    return created_user

@router.put('/update_user')
def update_user(
    user_id_to_update: int,
    user_update_details: UserUpdate,
    session: DB_SESSION,
    current_user:Annotated[dict, Depends(get_current_user)]):

    user_id_from_token = current_user.get("user_id")
    if user_id_from_token == user_id_to_update:
        updated_user = update_user_by_id(user_id_to_update, user_update_details, session)
        return updated_user
    else:
        raise HTTPException(
            status_code=403,
            detail="You are you not allowed to update other's id details."
        )
    
@router.delete("/delete_user")
def delete_user(
    session: DB_SESSION,
    admin: dict = Depends(get_current_admin), 
    user_id_to_delete: int = Query(..., description="ID of the user to delete")
    ):
    deleted_user = delete_user_by_id(user_id_to_delete, session)
    return deleted_user

@router.post("/login")
def admin_login(
                credential: Annotated[OAuth2PasswordRequestForm, Depends(OAuth2PasswordRequestForm)],
                session:DB_SESSION
                ):
    
    username = credential.username
    password = credential.password
    

    admin_or_user_id = admin_or_user(username, password, session)
    return admin_or_user_id

@router.get('/get-all-users')
def get_all_users(
    session: DB_SESSION,
    current_admin:dict = Depends(get_current_admin)
    ):

    users = fetch_all_users(session)
    return {"users": users}

@router.get('/get-token')
def get_token(session: DB_SESSION, email: str):

    generated_token = create_access_token({"sub": email})
    admin_verification =get_current_admin(generated_token)
    return admin_verification

@router.post('/add_admin')
def add_sub_admin(
    sub_admin_detail: SubAdmin,
    session: DB_SESSION,
    authority:Annotated[dict, Depends(get_current_admin
    )]):
    admin_to_create = sub_admin(sub_admin_detail, session)
    return admin_to_create