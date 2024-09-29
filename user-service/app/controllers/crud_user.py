from sqlmodel import Session, select
from app.models.user_models import UserModel, User, UserUpdate

from app.db.db_connector import DB_SESSION
from fastapi import HTTPException

def user_add(user_detail: User, session: DB_SESSION):
    user_email = user_detail.user_email
    users = session.exec(select(User))   
    for user in users:
        if user.user_email == user_email:
            raise HTTPException(
                status_code=404, detail="email already existed"
            )
    session.add(user_detail)
    session.commit()
    session.refresh(user_detail)    
    return user_detail
    
def get_user_by_id(user_id:int,session: DB_SESSION):    
    user = session.exec(select(User).where(User.user_id==user_id)).first()
    
    if user:
        return user
    
    raise HTTPException(
            status_code=404, detail="no user exits with this id"
            )

def update_user_by_id(user_id:int,user_update_details: UserUpdate,session: DB_SESSION):    
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
    


def delete_user_by_id(user_id_to_delete:int,session: DB_SESSION):    
    user = session.exec(select(User).where(User.user_id==user_id_to_delete)).first()
    if not user:    
        raise HTTPException(
            status_code=404, detail="no user exits with this id"
            )
    user_email = user.user_email        
    session.delete(user)
    session.commit()
    return f"User with id {user_id_to_delete} and email {user_email} has been deleted"
    




