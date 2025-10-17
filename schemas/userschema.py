from pydantic import BaseModel, EmailStr,constr,field_validator
from typing import Optional
from typing import Annotated
import re
class UserBase(BaseModel):
    name: str
    email: EmailStr
    mobile_number: str
    @field_validator("mobile_number")
    @classmethod
    def validate_mobile_number(cls, v):
        if not re.fullmatch(r"\d{10}", v):
            raise ValueError("Mobile number must contain exactly 10 digits")
        return v

    @field_validator("email")
    @classmethod
    def validate_email_domain(cls, v):
        allowed_domains = ("gmail.com", "yahoo.com", "outlook.com","gitam.in")
        domain = v.split("@")[-1].lower()
        if domain not in allowed_domains:
            raise ValueError("Email domain must be Gmail, Yahoo, or Outlook")
        return v
    


class UserInfo(BaseModel):
    id: int
    name: str
    email: str
    mobile_number: Optional[str] = None

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: str
    password: str

class UserCreate(UserBase):
    password: str
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if not (8 <= len(v) <= 72):
            raise ValueError("Password must be between 8 and 72 characters")
        return v



class UserResponse(UserBase):
    id: int
    role: str

    class Config:
        from_attributes = True
