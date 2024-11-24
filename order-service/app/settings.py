from starlette.config import Config

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

DATABASE_URL = config("DATABASE_URL")
SECRET_KEY = config("SECRET_KEY") 
ALGORITHM = config("ALGORITHM")