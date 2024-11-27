from typing import Annotated
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt,  JWTError, ExpiredSignatureError
from app.settings import ALGORITHM, SECRET_KEY


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://127.0.0.1:8081/login")

def admin_validate_token(token: Annotated[str, Depends(oauth2_scheme)]):
    print(token)
    validation = verify_token(token, role="admin")
    return validation
    
def verify_token(token: str, role : str):
    try:
        payload = jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM])
        print(payload)
        if payload.get("role") != role: 
            raise HTTPException(
                status_code=403, 
                detail=f"{role.capitalize()} access required"
                )
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
            detail=f"{role.capitalize()} access required"
        )
