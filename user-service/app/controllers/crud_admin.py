from sqlmodel import Session, select
from app.models.user_models import User
from app.models.admin_model import Admin
from app.db.db_connector import DB_SESSION,get_session
from fastapi import HTTPException
from passlib.context import CryptContext

ADMIN_EMAIL = "khazir@khazir.com"
ADMIN_PASSWORD = "khazirpassword"

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def create_initial_admin(email:str, password:str):
    
    hashed_password =pwd_context.hash(password)
    
    session = next(get_session())
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

def admin_authentication(admin_email:str, admin_password:str,session: DB_SESSION):
    admin = session.exec(select(Admin).where(Admin.admin_email==admin_email)).first()
    if not admin or not pwd_context.verify(admin_password, admin.admin_password):
        raise HTTPException(
            status_code=403,
            detail="Invalid admin credentials."
        )
    return admin, session




# def admin_authentication(user_id: int, session: DB_SESSION):
#     user = session.exec(select(User).where(User.user_id == user_id)).first()
    
#     if not user or not user.is_admin:
#         raise HTTPException(
#             status_code=403, detail="Admin access required."
#         )
#     return user, session




