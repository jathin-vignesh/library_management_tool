from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from db import get_db
from utils.security import decode_access_token
from models.models import User


from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    payload = decode_access_token(token)
    user = db.query(User).filter(User.id == payload["user_id"]).first()
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
