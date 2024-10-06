from fastapi import FastAPI
from app.routes.inventory_routes import router


app: FastAPI = FastAPI(
    version="0.0.0",
    servers=[
        {
            "url":"http://127.0.0.1.8002",
            "description": "Development Server"
        }
    ]
)



app.include_router(router=router)