from sqlmodel import Session, select
from app.models.user_models import UserModel, User, UserUpdate
from app.db.db_connector import DB_SESSION
from app.helpers.jwt_helper import create_access_token, oath2_scheme, verify_token
from fastapi import HTTPException, Depends
from passlib.context import CryptContext
from typing import Annotated

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def user_add(user_detail: User, session: Session):

    existing_user = session.exec(select(User).where(User.user_email== user_detail.user_email)).first()   
    if existing_user:
        raise HTTPException(
            status_code=409, detail="email already existed"
            )
   
    session.add(user_detail)
    session.commit()
    session.refresh(user_detail)    
    return user_detail
    
def get_user_by_id(user_id:int,session: Session):    
    user = session.exec(select(User).where(User.user_id==user_id)).first()
    
    if user:
        return user
    
    raise HTTPException(
            status_code=404, detail="no user exits with this id"
            )

def update_user_by_id(user_id:int,user_update_details: UserUpdate,session: Session):    
    user = session.exec(select(User).where(User.user_id==user_id)).first()
    if not user:
        raise HTTPException(
            status_code=404, detail="no user exits with this id"
            )
    if user_update_details.user_name is not None:
        user.user_name = user_update_details.user_name
    if user_update_details.phone_num is not None:
        user.phone_num = user_update_details.phone_num
    if user_update_details.user_password is not None:
        user.user_password = user_update_details.user_password
        
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return user
    


def delete_user_by_id(user_id_to_delete:int,session: Session):    
    user = session.exec(select(User).where(User.user_id==user_id_to_delete)).first()
    if not user:    
        raise HTTPException(
            status_code=404, detail="no user exits with this id"
            )
    user_email = user.user_email        
    session.delete(user)
    session.commit()
    return f"User with id {user_id_to_delete} and email {user_email} has been deleted"
    

def fetch_all_users(session: Session):
    users = session.exec(select(User)).all()
    return users

def user_authentication(username: str, password: str, session: Session):
    user = session.exec(select(User).where(User.user_email==username)).first()
    if not user:
        raise HTTPException(
            status_code=404, detail="no user exits with this id"
            )
    elif not pwd_context.verify(password, user.user_password):
        raise HTTPException(
            status_code=404, 
            detail="incorrect password"
        )
    access_token = create_access_token({"sub": username, "role": "user"})
    return {"access_token":access_token}

def get_current_user(token: Annotated[str, Depends(oath2_scheme)]):
    try:
        payload = verify_token(token)
    except HTTPException as e:
        if e.detail == "Token has expired":
            raise HTTPException(
                status_code=401, 
                detail="Token has expired, please log in again."
            )
        else:
            raise e
    
    if payload.get("role") != "user":
        raise HTTPException(
            status_code=403, 
            detail="User access required"
        )
    return payload