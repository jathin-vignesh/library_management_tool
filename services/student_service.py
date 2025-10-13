from sqlalchemy.orm import Session
from models.models import Book, BorrowRecord
from fastapi import HTTPException, status
from datetime import datetime, timezone

# ----------------- VIEW AVAILABLE BOOKS -----------------
def get_available_books(db: Session):
    return db.query(Book).filter(Book.available_copies > 0).all()

# ----------------- BORROW BOOK -----------------
def borrow_book(db: Session, user_id: int, book_id: int):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    if book.available_copies <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No copies available")

    # Check if already borrowed
    existing_record = db.query(BorrowRecord).filter(
        BorrowRecord.user_id == user_id,
        BorrowRecord.book_id == book_id,
        BorrowRecord.is_returned == False
    ).first()
    if existing_record:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book already borrowed")

    record = BorrowRecord(user_id=user_id, book_id=book_id)
    db.add(record)
    book.available_copies -= 1
    db.commit()
    db.refresh(record)
    return record

# ----------------- RETURN BOOK -----------------
def return_book(db: Session, user_id: int, book_id: int):
    record = db.query(BorrowRecord).filter(
        BorrowRecord.user_id == user_id,
        BorrowRecord.book_id == book_id,
        BorrowRecord.is_returned == False
    ).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active borrow record found")

    record.is_returned = True
    record.return_date = datetime.now(timezone.utc)

    book = db.query(Book).filter(Book.id == book_id).first()
    book.available_copies += 1

    db.commit()
    db.refresh(record)
    return record

# ----------------- VIEW BORROW HISTORY -----------------
def view_borrow_history(db: Session, user_id: int):
    return db.query(BorrowRecord).filter(
        BorrowRecord.user_id == user_id
    ).all()
