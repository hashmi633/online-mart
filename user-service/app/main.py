from fastapi import FastAPI
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from app.routes.user_routes import router
from app.db.db_connector import create_db_and_tables
from app.crud.crud_admin import initialize_admin
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app:FastAPI)->AsyncGenerator[None, None]:
    print("Starting Applicaton...!")
    # task = asyncio.create_task(consume_messages('todos2', 'broker:19092'))
    create_db_and_tables()
    initialize_admin()
    print("Application started with admin initialized.")
    yield

app : FastAPI = FastAPI(lifespan=lifespan, title="User Service",
    version="0.0.0",
    servers=[
        {
            "url": "http://127.0.0.1:8081", # ADD NGROK URL Here Before Creating GPT Action
            "description": "Development Server"
        }
        ])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify a list of allowed origins (e.g., ["http://127.0.0.1:8002"])
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


app.include_router(router=router)

