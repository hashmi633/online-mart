from fastapi import FastAPI
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from app.routes import user_routes
from app.db.db_connector import create_db_and_tables
from app.controllers.crud_admin import initialize_admin

@asynccontextmanager
async def lifespan(app:FastAPI)->AsyncGenerator[None, None]:
    print("Starting Applicaton...!")
    # task = asyncio.create_task(consume_messages('todos2', 'broker:19092'))
    create_db_and_tables()
    initialize_admin()
    print("Application started with admin initialized.")
    yield

app : FastAPI = FastAPI(lifespan=lifespan, title="Hello World",
    version="0.0.0",
    servers=[
        {
            "url": "http://127.0.0.1:8081", # ADD NGROK URL Here Before Creating GPT Action
            "description": "Development Server"
        }
        ])

app.include_router(router=user_routes.router)


@app.get('/bs')
def welcome():
    # print("Welcome to user interface")
    return {"Hello":"Welcome to User Service"}