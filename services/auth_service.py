from sqlalchemy.orm import Session
from models.models import User
from schemas.userschema import UserCreate, UserResponse
from fastapi import HTTPException, status, BackgroundTasks
from utils.security import create_access_token,create_refresh_token,decode_refresh_token
from utils.email_utils import send_registration_email
import bcrypt
from jose import JWTError, jwt
import os
def hash_password(password: str) -> str:
    password_bytes = password.strip().encode("utf-8")[:72]
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    plain_bytes = plain_password.strip().encode("utf-8")[:72]
    return bcrypt.checkpw(plain_bytes, hashed_password.encode("utf-8"))

def register_user(db: Session, background_tasks: BackgroundTasks, user: UserCreate) -> UserResponse:
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    hashed_password = hash_password(user.password)
    db_user = User(
        name=user.name,
        email=user.email,
        mobile_number=user.mobile_number,
        password=hashed_password,
        role="student"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    send_registration_email(background_tasks, user.email, user.name)
    return db_user

def register_admin_user(db: Session, user: UserCreate) -> UserResponse:
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    hashed_password = hash_password(user.password)
    db_user = User(
        name=user.name,
        email=user.email,
        mobile_number=user.mobile_number,
        password=hashed_password,
        role="admin"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"user_id": user.id, "role": user.role})
    refresh_token = create_refresh_token({"user_id": user.id, "role": user.role})

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def refresh_access_token(refresh_token: str):
    payload = decode_refresh_token(refresh_token)
    new_access_token = create_access_token({"user_id": payload["user_id"], "role": payload["role"]})
    return {"access_token": new_access_token, "token_type": "bearer"}