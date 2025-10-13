from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from db import get_db
from utils.security import decode_access_token
from models.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# ---------------- Get current user ----------------
def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    data = decode_access_token(token)
    user = db.query(User).filter(User.id == data["user_id"]).first()  # now works
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# ---------------- Role-based dependency ----------------
def admin_required(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return current_user

def student_required(current_user: User = Depends(get_current_user)):
    if current_user.role not in ["student", "admin"]:
        raise HTTPException(status_code=403, detail="Student privileges required")
    return current_user
