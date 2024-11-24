from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from fastapi import Depends,HTTPException
from jose import jwt, JWTError
from app.settings import SECRET_KEY,ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://127.0.0.1:8081/login")

def validate_token(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=401, 
            detail=f"Could not validate due to error: {e}")
    