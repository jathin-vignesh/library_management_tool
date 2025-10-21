from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from schemas.userschema import UserInfo
class BorrowRecordBase(BaseModel):
    book_id: int


class BorrowRecordCreate(BorrowRecordBase):
    user_id: int


class BorrowRecordResponse(BaseModel):
    id: int
    user_id: int
    book_id: int
    borrow_date: datetime
    deadline_date: datetime
    return_date: Optional[datetime] = None
    is_returned: bool

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M") 
        }


class AdminBorrowRecordResponse(BaseModel):
    id: int
    book_id: int
    borrow_date: datetime
    deadline_date: datetime
    return_date: Optional[datetime] = None
    is_returned: bool
    user: UserInfo

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M") 
        }
