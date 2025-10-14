import smtplib
from email.message import EmailMessage
from fastapi import BackgroundTasks
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("MAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

def send_email(to_email: str, subject: str, body: str):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg.set_content(body)

    # Using port 587 with STARTTLS
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()                # Optional, but good practice
        smtp.starttls()            # Upgrade connection to secure
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

def send_registration_email(background_tasks: BackgroundTasks, to_email: str, username: str):
    background_tasks.add_task(
        send_email,
        to_email=to_email,
        subject="Registration Successful",
        body=f"Hello {username}, you have successfully registered to library!"
    )
