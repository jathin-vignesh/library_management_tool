from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BorrowRecordBase(BaseModel):
    book_id: int


class BorrowRecordCreate(BorrowRecordBase):
    user_id: int


class BorrowRecordResponse(BaseModel):
    id: int
    user_id: int
    book_id: int
    borrow_date: datetime
    return_date: Optional[datetime] = None
    is_returned: bool

    class Config:
        from_attributes = True
