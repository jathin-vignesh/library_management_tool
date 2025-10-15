from pydantic import BaseModel, EmailStr,constr
from typing import Optional
from typing import Annotated
class UserBase(BaseModel):
    name: str
    email: EmailStr
    mobile_number: Optional[str] = None


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
    password: Annotated[str, constr(min_length=4, max_length=72)]


class UserResponse(UserBase):
    id: int
    role: str

    class Config:
        from_attributes = True
