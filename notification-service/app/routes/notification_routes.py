from fastapi import APIRouter
from app.email_test.smtp import to_send_email

router = APIRouter()

@router.get("/")
def welcome():
    return "Welcome to Notification Service"

@router.post("/send-email")
def send_email(to_email, subject, body):
    email = to_send_email(to_email, subject, body)
    return email