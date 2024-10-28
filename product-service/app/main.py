from fastapi import FastAPI
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from app.db.db_connector import create_db_and_tables

@asynccontextmanager
async def lifespan(app:FastAPI)->AsyncGenerator[None, None]:
    print("Starting Applicaton...!")
    # task = asyncio.create_task(consume_messages('todos2', 'broker:19092'))
    create_db_and_tables()
    # initialize_admin()
    print("Product service started")
    yield


app: FastAPI = FastAPI(lifespan=lifespan, title="Product Service",
    version="0.0.0",
    servers=[
        {
            "url": "http://127.0.0.1:8003", # ADD NGROK URL Here Before Creating GPT Action
            "description": "Development Server"
        }
    ]
)

@app.get("/")
def welcome():
    return {"Hello":"Welcome to Product Service"}


