from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from schemas.bookschema import BookCreate, BookResponse
from schemas.userschema import UserResponse
from schemas.borrowrecordschema import BorrowRecordResponse
from services import admin_service
from db import get_db
from utils.dependencies import admin_required  # ensures only admin can access

router = APIRouter(prefix="/admin")

# ---------------- Add a new book ----------------
@router.post("/books/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def add_book(
    book: BookCreate,
    db: Session = Depends(get_db),
    current_admin = Depends(admin_required)
):
    return admin_service.add_book(db, book)

# ---------------- Get all books ----------------
@router.get("/books/", response_model=List[BookResponse])
def get_all_books(
    db: Session = Depends(get_db),
    current_admin = Depends(admin_required)
):
    return admin_service.get_all_books(db)

# ---------------- Update (PATCH) a book by ID ----------------
@router.patch("/books/{book_id}", response_model=BookResponse)
def update_book(
    book_id: int,
    book_data: dict,
    db: Session = Depends(get_db),
    current_admin = Depends(admin_required)
):
    return admin_service.update_book(db, book_id, book_data)

# ---------------- Delete a book ----------------
@router.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_admin = Depends(admin_required)
):
    admin_service.delete_book(db, book_id)
    return {"message": "Book deleted successfully"}

# ---------------- Get all users (students) ----------------
@router.get("/users/", response_model=List[UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    current_admin = Depends(admin_required)
):
    return admin_service.get_all_users(db)

@router.get("/borrowHist",response_model=List[BorrowRecordResponse])
def get_all_borrow(db: Session = Depends(get_db),
    current_admin = Depends(admin_required)):
    return admin_service.get_borrow_table(db)