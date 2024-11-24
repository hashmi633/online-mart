from fastapi import APIRouter
from app.email_test.smtp import to_send_email
from app.oath2 import validate_token
from typing import Annotated
from fastapi import Depends

router = APIRouter()

@router.get("/")
def welcome():
    return "Welcome to Notification Service"

@router.post("/send-email")
def send_email(to_email, subject, body):
    email = to_send_email(to_email, subject, body)
    return email

@router.get("/get-token")
def get_token(token: Annotated[str, Depends(validate_token)]):
    email = token.get("sub")
    return email