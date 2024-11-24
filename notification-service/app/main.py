from fastapi import FastAPI
from app.routes.notification_routes import router
from typing import AsyncGenerator
from app.kafka.notification_consumer import consume_order_notification
import asyncio

async def lifespan(app: FastAPI)->AsyncGenerator[None,None]:
    print("Starting Applicaton...!")
    task =asyncio.create_task(consume_order_notification())
    print("Notification Application Started.")
    yield


app : FastAPI = FastAPI(lifespan=lifespan, title="Notification Service")

app.include_router(router=router)