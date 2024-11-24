from sqlmodel import Session, select
from app.models.user_models import UserModel, User, UserUpdate
from app.models.admin_model import Admin
from app.crud.crud_admin import get_current_user_by_role
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

def get_current_user(token: Annotated[str, Depends(oath2_scheme)]):
    return get_current_user_by_role(token, role="user")
    
def update_user_by_id(user_id_to_update:int, user_update_details: UserUpdate, session: Session):    

        user = session.exec(select(User).where(User.user_id==user_id_to_update)).first()
        
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
    # else:
    #     if not user:
    #         raise HTTPException(
    #             status_code=404, detail="no user exits with this id"
    #             )

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

def admin_or_user(username: str, password: str, session: Session):
    
    admin = session.exec(select(Admin).where(Admin.admin_email==username)).first()
    user = session.exec(select(User).where(User.user_email == username)).first()

    if admin and pwd_context.verify(password, admin.admin_password):
        access_token = create_access_token({"sub": username, "role": "admin", "user_id": admin.admin_id})
        return {"access_token": access_token, "token_type":"Bearer"}
    elif user and password == user.user_password:
        access_token = create_access_token({"sub": username, "role": "user", "user_id": user.user_id, "user_name": user.user_name})
        print(access_token)
        return {"access_token": access_token, "token_type":"Bearer"}