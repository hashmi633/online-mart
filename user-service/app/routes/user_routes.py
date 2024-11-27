from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Annotated
from app.crud.crud_user import user_add,get_user_by_id,delete_user_by_id,update_user_by_id, fetch_all_users , get_current_user, admin_or_user, login_of_user
from app.crud.crud_admin import get_admin_access, sub_admin
from app.db.db_connector import DB_SESSION
from app.models.user_models import User,UserUpdate
from app.models.admin_model import SubAdmin
from fastapi.security import OAuth2PasswordRequestForm
from app.helpers.jwt_helper import oath2_scheme, create_access_token, verify_token
from sqlmodel import select
from aiokafka import AIOKafkaProducer
from app.helpers.kafka import get_kafka_producer
import json

router = APIRouter()

@router.get("/")
def welcome():
    return {"Hello":"Welcome to User Service"}

@router.get("/get_user")
def get_user(user_id: int, session: DB_SESSION, token: str = Depends(oath2_scheme)):
    user_to_get = get_user_by_id(user_id, session)
    return user_to_get

@router.post('/add_user')
async def add_user(user: User,
             producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)],
             session: DB_SESSION):
    
    created_user = user_add(user, session)
    user_data = {field: getattr(created_user, field) for field in created_user.dict()}
    user_json = json.dumps(user_data).encode("utf-8")
    await producer.send_and_wait("users", user_json)
    return created_user

@router.put('/update_user')
def update_user(
    user_update_details: UserUpdate,
    session: DB_SESSION,
    token:Annotated[dict, Depends(get_current_user)]):

    user_id = token.get("user_id")
    if user_id:
        updated_user = update_user_by_id(user_id, user_update_details, session)
        return updated_user
    else:
        raise HTTPException(
            status_code=403,
            detail="Authentication Require"
        )
    
@router.delete("/delete_user")
def delete_user(
    session: DB_SESSION,
    admin: dict = Depends(get_admin_access), 
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
    

    login = admin_or_user(username, password, session)
    return login

@router.post("/user-login")
def user_login(
                credential: Annotated[OAuth2PasswordRequestForm, Depends(OAuth2PasswordRequestForm)],
                session:DB_SESSION
                ):
    
    username = credential.username
    password = credential.password
    

    login = login_of_user(username, password, session)
    return login


@router.get('/get-all-users')
def get_all_users(
    session: DB_SESSION,
    admin_token:dict = Depends(get_admin_access)
    ):

    users = fetch_all_users(session)
    return {"users": users}

@router.get('/get-token')
def get_token(session: DB_SESSION, email: str):
    generated_token = create_access_token({"sub": email, "role": "admin"})
    admin_verification =get_admin_access(generated_token)
    return {"token": generated_token, "payload": admin_verification}

@router.post('/add_admin')
def add_sub_admin(
    sub_admin_detail: SubAdmin,
    session: DB_SESSION,
    authority:Annotated[dict, Depends(get_admin_access
    )]):
    admin_to_create = sub_admin(sub_admin_detail, session)
    return admin_to_create