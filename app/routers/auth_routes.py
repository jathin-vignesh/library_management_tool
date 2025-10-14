from fastapi import APIRouter,Depends,BackgroundTasks
from schemas.userschema import UserCreate, UserResponse,UserLogin
from services.auth_service import register_user,authenticate_user,register_admin_user  # logic in services
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from db import get_db
from utils.email_utils import send_registration_email
router = APIRouter(prefix="/auth")

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate,background_tasks: BackgroundTasks,db: Session = Depends(get_db)):
    send_registration_email(background_tasks, user.email, user.name)
    return register_user(db, user)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return authenticate_user(db, form_data.username, form_data.password)

@router.post("/register/admin", response_model=UserResponse)
def register_admin(user: UserCreate, db: Session = Depends(get_db)):
    return register_admin_user(db, user)