import logging
import threading
import time
from datetime import datetime

from croniter import croniter

from patronx.tasks import cleanup_old_backups, run_backup_job

# Set up basic logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def start_backup_scheduler(cron_expr: str) -> threading.Thread:
    def _runner() -> None:
        logger.info(f"Backup scheduler started with cron expression: {cron_expr}")
        itr = croniter(cron_expr, datetime.utcnow())
        while True:
            next_ts = itr.get_next(datetime)
            delay = (next_ts - datetime.utcnow()).total_seconds()
            logger.info(f"Next backup scheduled at {next_ts} (in {delay:.2f} seconds)")
            if delay > 0:
                time.sleep(delay)
            logger.info("Triggering backup job...")
            run_backup_job.send()
            logger.info("Backup job triggered.")

    t = threading.Thread(target=_runner, daemon=True)
    t.start()
    logger.info("Backup scheduler thread started.")
    return t


def start_cleanup_scheduler(cron_expr: str) -> threading.Thread:
    """Start a background thread that periodically cleans up old backups."""

    def _runner() -> None:
        logger.info(
            f"Cleanup scheduler started with cron expression: {cron_expr}"
        )
        itr = croniter(cron_expr, datetime.utcnow())
        while True:
            next_ts = itr.get_next(datetime)
            delay = (next_ts - datetime.utcnow()).total_seconds()
            logger.info(
                f"Next cleanup scheduled at {next_ts} (in {delay:.2f} seconds)"
            )
            if delay > 0:
                time.sleep(delay)
            logger.info("Triggering cleanup job...")
            cleanup_old_backups.send()
            logger.info("Cleanup job triggered.")

    t = threading.Thread(target=_runner, daemon=True)
    t.start()
    logger.info("Cleanup scheduler thread started.")
    return t