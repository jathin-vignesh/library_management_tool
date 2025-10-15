from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("MAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

conf = ConnectionConfig(
    MAIL_USERNAME=EMAIL_ADDRESS,
    MAIL_PASSWORD=EMAIL_PASSWORD,
    MAIL_FROM=EMAIL_ADDRESS,
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

fm = FastMail(conf)

def send_registration_email(background_tasks: BackgroundTasks, to_email: str, username: str):
    message = MessageSchema.model_construct(
        subject="Registration Successful",
        recipients=[to_email],
        body=f"Hello {username}, you have successfully registered to the library!",
        subtype=MessageType.plain
    )
    background_tasks.add_task(fm.send_message, message)

async def send_overdue_email(to_email: str, book_title: str, due_date: datetime):
    message = MessageSchema.model_construct(
        subject="Library Book Return Reminder",
        recipients=[to_email],
        body=f"""
Dear Student,

The book "{book_title}" was due on {due_date.strftime('%Y-%m-%d')}.
Please return it to the library as soon as possible to avoid fines.

Regards,
Library Team
""",
        subtype=MessageType.plain
    )
    await fm.send_message(message)


async def send_borrow_email(to_email: str, username: str, book_title: str, borrow_date: datetime, deadline_date: datetime):
    message = MessageSchema.model_construct(
        subject="Library Book Borrowed",
        recipients=[to_email],
        body=f"""
Hello {username},

You have successfully borrowed the book titled **"{book_title}"** from the library.

Borrow Date: {borrow_date.strftime('%Y-%m-%d')}
Due Date: {deadline_date.strftime('%Y-%m-%d')}

Please make sure to return the book on or before the due date to avoid any fines.

Happy Reading!  
Library Team
""",
        subtype=MessageType.plain
    )
    await fm.send_message(message)

async def send_return_email(to_email: str, username: str, book_title: str, return_date: datetime):
    message = MessageSchema.model_construct(
        subject="Library Book Returned",
        recipients=[to_email],
        body=f"""
Hello {username},

You have successfully returned the book titled **"{book_title}"** to the library.

Return Date: {return_date.strftime('%Y-%m-%d')}

Thank you for using the library services. We hope you enjoyed reading!

Regards,  
Library Team
""",
        subtype=MessageType.plain
    )
    await fm.send_message(message)