from fastapi import FastAPI
from contextlib import asynccontextmanager
from typing import AsyncGenerator
# from app.models.products_models import Product
from app.db.db_connector import create_db_and_tables
import asyncio
from app.kafka_product import consume_products_requests
from app.routes.product_routes import router

@asynccontextmanager
async def lifespan(app:FastAPI)->AsyncGenerator[None, None]:
    print("Starting Applicaton...!")
    task1 = asyncio.create_task(consume_products_requests())
    create_db_and_tables()
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

app.include_router(router=router)



