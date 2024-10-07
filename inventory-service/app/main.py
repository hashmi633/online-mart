from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes.inventory_routes import router
from typing import AsyncGenerator
from app.db.db_connector import create_db_and_tables

@asynccontextmanager
async def lifespan(app:FastAPI)->AsyncGenerator[None, None]:
    print("Starting Applicaton...!")
    create_db_and_tables()
    print("Inventory Application Started.")
    yield

app: FastAPI = FastAPI(lifespan=lifespan,
    version="0.0.0",
    servers=[
        {
            "url":"http://127.0.0.1:8002",
            "description": "Development Server"
        }
    ]
)



app.include_router(router=router)