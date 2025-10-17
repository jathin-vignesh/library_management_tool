from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from db import Base 

# USER MODEL
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    mobile_number = Column(String, nullable=False)
    password = Column(String, nullable=False)  
    role = Column(String, default="student", nullable=False)  

    # Relationship with cascade
    borrow_records = relationship(
        "BorrowRecord",
        back_populates="user",
        cascade="all, delete-orphan",  # ORM cascade
        passive_deletes=True           # DB handles deletion
    )


# BOOK MODEL
class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    isbn = Column(String(13), unique=True, index=True, nullable=False)
    available_copies = Column(Integer, default=1, nullable=False)

    # Relationship with cascade
    borrow_records = relationship(
        "BorrowRecord",
        back_populates="book",
        cascade="all, delete-orphan",
        passive_deletes=True
    )


# BORROW RECORD MODEL
class BorrowRecord(Base):
    __tablename__ = "borrow_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    borrow_date = Column(DateTime(timezone=True), server_default=func.now())
    return_date = Column(DateTime(timezone=True), nullable=True)
    deadline_date = Column(DateTime(timezone=True), nullable=False, default=func.now())
    is_returned = Column(Boolean, default=False)

    # Relationships
    user = relationship("User", back_populates="borrow_records")
    book = relationship("Book", back_populates="borrow_records")
