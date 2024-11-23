from starlette.config import Config

try:    
    config = Config(".env")
except FileNotFoundError:
    config = Config()

EMAIL = config("EMAIL_USERNAME")
PASSWORD = config("EMAIL_PASSWORD")