from fastapi import FastAPI
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from app.db.db_connector import create_db_and_tables
from app.routes.order_routes import router

@asynccontextmanager
async def lifespan(app: FastAPI)->AsyncGenerator[None, None]:
    print("Starting Order Service")
    create_db_and_tables()
    print("Order Service Started")
    yield

app : FastAPI = FastAPI(lifespan=lifespan, title="Order Service",
                        version="0.0.0",
                        servers=[
                            {
                                "url":"http://127.0.0.1:8004",
                                "description": "Development Server"
                            }
                        ]
                        )

app.include_router(router=router)


