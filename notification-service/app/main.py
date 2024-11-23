from fastapi import FastAPI
from app.routes.notification_routes import router

app : FastAPI = FastAPI(title="Notification Service")

app.include_router(router=router)