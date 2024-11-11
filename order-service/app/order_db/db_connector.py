from app.settings import DATABASE_URL
from sqlmodel import create_engine, Session, SQLModel
from fastapi import Depends
from typing import Annotated

connection_string = str(DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)

engine = create_engine(
    connection_string,
    pool_pre_ping=True,
    echo=True,
    pool_recycle=300
)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables()->None:
    SQLModel.metadata.create_all(engine)
    
DB_SESSION = Annotated[Session, Depends(get_session)]   
