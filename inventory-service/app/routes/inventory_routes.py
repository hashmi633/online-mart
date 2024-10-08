from fastapi import APIRouter, Depends, HTTPException
from app.models.inventory_models import Category,Warehouse,InventoryItem
from app.db.db_connector import DB_SESSION, get_session
from typing import Annotated
from sqlmodel import Session
from jose import jwt,  JWTError
from app.jwt_helper import SECRET_KEY, ALGORITHM
from app.shared_helper import validate_token
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://127.0.0.1:8081/login")

@router.get('/')
def welcome():
    return{"Hello":"Welcome to Inventory Service"}

@router.post('/add_category')
def add_category(category_name: str, token: Annotated[str, Depends(oauth2_scheme)]):
    # This token is now automatically pulled from the Authorization header
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Could not validate credentials")