from app.settings import DATABASE_URL
from sqlmodel import  create_engine, SQLModel,Session
from typing import Annotated
from fastapi import Depends


connection_string = str(DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)

engine = create_engine(
    connection_string,
    pool_pre_ping = True,
    echo=True,
    pool_recycle=300
    )

def get_session():
    with Session(engine) as session:
        yield session

DB_SESSION = Annotated[Session, Depends(get_session)]   

def create_db_and_tables()->None:
    print("Creating tables...")
    print("Models in SQLModel.metadata:", SQLModel.metadata.tables.keys())
    SQLModel.metadata.create_all(engine)
    print("Created tables...")
    

