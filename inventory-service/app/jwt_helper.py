from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer



ALGORITHM = "HS256"
SECRET_KEY = "My-Secure-Key"
ACCESS_TOKEN_EXPIRATION_TIME: int = 10

oauth2_scheme = OAuth2PasswordBearer(tokenUrl= "user:8081/login")

# def verify_token(token: dict):
#     try:
#         payload = jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM])
#         return payload
#     except ExpiredSignatureError:
#         # Token is expired
#         raise HTTPException(
#             status_code=401,
#             detail="Token has expired"
#         )
#     except JWTError as e:
#         raise HTTPException(
#             status_code=401,
#             detail="Could not validate credentials"
#         )


