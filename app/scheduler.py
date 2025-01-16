from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.dal.dal import delete_inactive_urls
import logging

# Configure logging for the job
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_scheduled_jobs():
    scheduler = BackgroundScheduler()

    scheduler.add_job(
        func=delete_inactive_urls,
        trigger=IntervalTrigger(minutes=1),
        id="delete_inactive_urls_job",
        replace_existing=True,
    )
    scheduler.start()
    logger.info("Scheduler started and job added to delete inactive URLs every 1 minute.")
