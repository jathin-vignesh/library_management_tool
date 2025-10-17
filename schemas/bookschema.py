from pydantic import BaseModel,field_validator
from typing import Optional
import re
class BookBase(BaseModel):
    title: str
    author: str
    isbn: str
    available_copies: int = 1


class BookCreate(BookBase):
    @field_validator("isbn")
    @classmethod
    def validate_isbn(cls, v):
        length = len(str(v))
        if length not in (10, 13):
            raise ValueError("ISBN must be either 10 or 13 digits long")
        return v


class BookResponse(BookBase):
    id: int

    class Config:
        from_attributes = True

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None
    available_copies: Optional[int] = None
    
    @field_validator("isbn")
    @classmethod
    def validate_isbn(cls, v):
        if v is not None:
            # Remove any hyphens or spaces
            cleaned = re.sub(r"[-\s]", "", v)
            if not cleaned.isdigit() or not (10 <= len(cleaned) <= 13):
                raise ValueError("ISBN must be a numeric string with 10 to 13 digits")
        return v
