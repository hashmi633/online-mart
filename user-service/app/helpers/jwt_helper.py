from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import HTTPException


ALGORITHM = "HS256"
SECRET_KEY = "My-Secure-Key"
ACCESS_TOKEN_EXPIRATION_TIME: int = 10

oath2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def create_access_token(data : dict):
    encoded_data = data.copy()
    encoded_data_with_expire_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRATION_TIME)
    encoded_data.update({"exp": encoded_data_with_expire_time})
    encoded_jwt = jwt.encode(encoded_data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        # Token is expired
        raise HTTPException(
            status_code=401,
            detail="Token has expired"
        )
    except JWTError as e:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials"
        )


