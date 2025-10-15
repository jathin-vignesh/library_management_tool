from apscheduler.schedulers.background import BackgroundScheduler
from tasks.overdue import check_and_send_overdue_emails
from db import Session
import asyncio

def start_scheduler():
    scheduler = BackgroundScheduler()

    def job():
        print("Scheduler job triggered")
        db = Session()
        asyncio.run(check_and_send_overdue_emails(db))
        db.close()

    # Run once every day at midnight
    scheduler.add_job(job, "cron", hour=0, minute=0)
    scheduler.start()
