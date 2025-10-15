from sqlalchemy.orm import Session
from models.models import Book, User, BorrowRecord
from schemas.bookschema import BookCreate, BookResponse,BookUpdate
from schemas.userschema import UserResponse
from fastapi import HTTPException, status

# ----------------- BOOK OPERATIONS -----------------
def add_book(db: Session, book: BookCreate) -> BookResponse:
    existing_book = db.query(Book).filter(Book.isbn == book.isbn).first()
    if existing_book:
        raise HTTPException(status_code=400, detail="Book already exists")
    
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_all_books(db: Session):
    return db.query(Book).all()

def update_book(db: Session, book_id: int, book_data: BookUpdate):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    for key, value in book_data.dict(exclude_unset=True).items():
        setattr(book, key, value)

    db.commit()
    db.refresh(book)
    return book


def delete_book(db: Session, book_id: int):
    # Fetch the book
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    
    # Check for any active borrow records
    active_borrows = db.query(BorrowRecord).filter(
        BorrowRecord.book_id == book_id,
        BorrowRecord.is_returned == False
    ).count()
    
    if active_borrows > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Some copies are being borrowed, cannot delete the book"
        )
    
    # Delete the book if no active borrowings
    db.delete(book)
    db.commit()
    return


# ----------------- USER OPERATIONS -----------------
def get_all_users(db: Session):
    return db.query(User).all()

def get_borrow_table(db: Session):
    return db.query(BorrowRecord).all()

def get_activeBorrow_table(db: Session):
    records = db.query(BorrowRecord).filter(BorrowRecord.is_returned == False).all()
    return records