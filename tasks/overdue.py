from datetime import datetime, timezone
from sqlalchemy.orm import Session
from utils.email_utils import send_overdue_email
from models.models import BorrowRecord as Borrow
from fastapi import Depends
from db import get_db

async def check_and_send_overdue_emails(db: Session = Depends(get_db)):
    overdue_borrows = db.query(Borrow).filter(
        Borrow.is_returned == False,
        Borrow.deadline_date < datetime.now(timezone.utc)
    ).all()

    for borrow in overdue_borrows:
        user_email = borrow.user.email
        book_title = borrow.book.title
        due_date = borrow.deadline_date

        await send_overdue_email(user_email, book_title, due_date)