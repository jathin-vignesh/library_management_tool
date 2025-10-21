from sqlalchemy.orm import Session
from models.models import Book, BorrowRecord
from fastapi import HTTPException, status
from datetime import datetime, timezone,timedelta
from utils.email_utils import send_borrow_email, send_return_email

# ----------------- VIEW AVAILABLE BOOKS -----------------
def get_available_books(db: Session):
    return db.query(Book).filter(Book.available_copies > 0).all()

# ----------------- BORROW BOOK -----------------
async def borrow_book(db: Session, user_id: int, book_id: int):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    if book.available_copies <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No copies available")

    existing_record = db.query(BorrowRecord).filter(
        BorrowRecord.user_id == user_id,
        BorrowRecord.book_id == book_id,
        BorrowRecord.is_returned == False
    ).first()
    if existing_record:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book already borrowed")
    borrow_date = datetime.now(timezone.utc)
    deadline_date = borrow_date + timedelta(days=30)
    record = BorrowRecord(
        user_id=user_id,
        book_id=book_id,
        borrow_date=borrow_date,
        deadline_date=deadline_date
    )

    db.add(record)
    book.available_copies -= 1
    db.commit()
    db.refresh(record)
    await send_borrow_email(
    to_email=record.user.email,
    username=record.user.name,
    book_title=book.title,
    borrow_date=borrow_date,
    deadline_date=deadline_date
    )
    return record

# ----------------- RETURN BOOK -----------------
from datetime import datetime, timezone
from utils.email_utils import send_return_email  # make sure this is imported

async def return_book(db: Session, user_id: int, book_id: int):
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
    await send_return_email(
        to_email=record.user.email,
        username=record.user.name,
        book_title=book.title,
        return_date=record.return_date
    )

    return record

# ----------------- VIEW BORROW HISTORY -----------------
def view_borrow_history(db: Session, user_id: int):
    return db.query(BorrowRecord).filter(
        BorrowRecord.user_id == user_id
    ).all()

def view_active_borrow_history(db: Session, user_id: int):
    return db.query(BorrowRecord).filter(
        BorrowRecord.user_id == user_id,
        BorrowRecord.is_returned == False
    ).all()

#search book by name
def search_book_by_name(db: Session, book_name: str):
    normalized_input = "".join(book_name.lower().split())
    books = db.query(Book).all()
    for book in books:
        normalized_book_name = "".join(book.title.lower().split())
        if normalized_input in normalized_book_name:
            return book
    return None