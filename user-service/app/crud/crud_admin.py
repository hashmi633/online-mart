from sqlmodel import Session, select
from app.models.admin_model import Admin, SubAdmin
from app.db.db_connector import DB_SESSION,get_session
from fastapi import HTTPException
from passlib.context import CryptContext
from app.helpers.jwt_helper import create_access_token, oath2_scheme, verify_token
from fastapi import Depends
from typing import Annotated
from app.settings import ADMIN_EMAIL, ADMIN_PASSWORD

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def create_initial_admin(email:str, password:str):
    
    hashed_password = pwd_context.hash(password)
    
    with next(get_session()) as session:
        existing_admin = session.exec(select(Admin).where(Admin.admin_email==email)).first()
        if existing_admin:
            print("Admin already exists. Skipping creation.")
            return
        
        new_admin = Admin(admin_email=email,admin_password=hashed_password)
        session.add(new_admin)
        session.commit()
        session.refresh(new_admin)
        print(f"Admin user created with email: {email}")

def initialize_admin():
    create_initial_admin(ADMIN_EMAIL,ADMIN_PASSWORD)

def admin_authentication(admin_email:str, admin_password:str,session: Session):
    admin = session.exec(select(Admin).where(Admin.admin_email==admin_email)).first()
    if not admin:
        raise HTTPException(
            status_code=403,
            detail="Username does not exists"
        )
    elif not pwd_context.verify(admin_password, admin.admin_password):
        raise HTTPException(
            status_code=403,
            detail="Invalid password"
        )
    access_token = create_access_token({"sub": admin_email, "role": "admin"})
    return {"access_token": access_token, "token_type": "bearer"}

def get_admin_access(token: Annotated[str, Depends(oath2_scheme)]):
    print(token)
    return verify_token(token, role="admin")
    
def sub_admin(sub_admin_detail: SubAdmin, session: Session):
    admin = session.exec(select(SubAdmin).where(SubAdmin.admin_email == sub_admin_detail.admin_email)).first()
    if admin:
       raise HTTPException(
        status_code=402,
        detail="email aleady exists."
       ) 
    else: 
        session.add(sub_admin_detail)
        session.commit()
        session.refresh(sub_admin_detail)
    
    return sub_admin_detail