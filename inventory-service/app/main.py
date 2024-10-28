from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes.inventory_routes import router
from typing import AsyncGenerator
from app.db.db_connector import create_db_and_tables
from fastapi.middleware.cors import CORSMiddleware
from app.kafka_code import consume_messages
import asyncio



@asynccontextmanager
async def lifespan(app:FastAPI)->AsyncGenerator[None, None]:
    print("Starting Applicaton...!")
    create_db_and_tables()
    task = asyncio.create_task(consume_messages('users','broker:19092'))
    # print("Inventory Application Started.")
    yield

app: FastAPI = FastAPI(lifespan=lifespan, title="Inventory Service",
    version="0.0.0",
    servers=[
        {
            "url":"http://127.0.0.1:8002",
            "description": "Development Server"
        }
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify a list of allowed origins (e.g., ["http://127.0.0.1:8002"])
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


app.include_router(router=router)