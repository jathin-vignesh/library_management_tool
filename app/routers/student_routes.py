from fastapi import APIRouter, Depends, status,HTTPException
from sqlalchemy.orm import Session
from typing import List

from schemas.bookschema import BookResponse
from schemas.borrowrecordschema import BorrowRecordResponse
from services import student_service
from db import get_db
from utils.dependencies import student_required  # allows student or admin

router = APIRouter(prefix="/student")

# ---------------- View all available books ----------------
@router.get("/books/available", response_model=List[BookResponse])
def get_available_books(
    db: Session = Depends(get_db),
    current_user = Depends(student_required)
):
    return student_service.get_available_books(db)

#search book by name
@router.get("/search-book", response_model=BookResponse)
def search_book(book_name: str, db: Session = Depends(get_db),current_user = Depends(student_required)):
    book = student_service.search_book_by_name(db, book_name)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# ---------------- Borrow a book ----------------
@router.post("/borrow/{book_id}", response_model=BorrowRecordResponse)
async def borrow_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(student_required)
):
    user_id = current_user.id  # get ID from JWT token
    return await student_service.borrow_book(db, user_id, book_id)

# ---------------- Return a book ----------------
@router.post("/return/{book_id}", response_model=BorrowRecordResponse)
async def return_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(student_required)
):
    user_id = current_user.id
    return await student_service.return_book(db, user_id, book_id)

# ---------------- View student's borrow history ----------------
@router.get("/borrow/history", response_model=List[BorrowRecordResponse])
def view_borrow_history(
    db: Session = Depends(get_db),
    current_user = Depends(student_required)
):
    user_id = current_user.id
    return student_service.view_borrow_history(db, user_id)

@router.get("/active/borrow/history", response_model=List[BorrowRecordResponse])
def view_active_borrow_history(
    db: Session = Depends(get_db),
    current_user = Depends(student_required)
):
    user_id = current_user.id
    return student_service.view_active_borrow_history(db, user_id)