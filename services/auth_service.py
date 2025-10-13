from sqlalchemy.orm import Session
from models.models import User
from schemas.userschema import UserCreate, UserResponse
from passlib.context import CryptContext
from fastapi import HTTPException, status
from utils.security import create_access_token
import bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    password_bytes = password.strip().encode("utf-8")[:72]
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    plain_bytes = plain_password.strip().encode("utf-8")[:72]
    return bcrypt.checkpw(plain_bytes, hashed_password.encode("utf-8"))


def register_user(db: Session, user: UserCreate) -> UserResponse:
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Email already registered")

    hashed_password = hash_password(user.password)
    db_user = User(
        name=user.name,
        email=user.email,
        mobile_number=user.mobile_number,
        password=hashed_password,
        role="student"  # default role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def register_admin_user(db: Session, user: UserCreate) -> UserResponse:
    # Admin registration logic
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed_password = hash_password(user.password)
    db_user = User(
        name=user.name,
        email=user.email,
        mobile_number=user.mobile_number,
        password=hashed_password,
        role="admin"  # admin role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"user_id": user.id, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}