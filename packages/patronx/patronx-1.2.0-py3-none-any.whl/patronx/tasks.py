import os
from datetime import datetime
from pathlib import Path
import logging
import remoulade
from remoulade import actor
from remoulade.brokers.rabbitmq import RabbitmqBroker

from datetime import timedelta

from patronx.backup import run_backup
from patronx.config import BackupConfig

BROKER_URL = os.getenv("AMQP_URL", "amqp://guest:guest@localhost:5672/")
broker = RabbitmqBroker(url=BROKER_URL)
remoulade.set_broker(broker)

logger = logging.getLogger(__name__)
# ensure all actors defined below are associated with the broker

def _backup_path(cfg: BackupConfig) -> Path:
    stamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    return Path(cfg.backup_dir) / f"{cfg.database}-{stamp}.dump"


@actor(
    queue_name="backups",
    max_retries=5,
)
def run_backup_job(*, show_progress: bool = False) -> str:
    logger.info("Starting backup job (show_progress=%s)", show_progress)
    cfg = BackupConfig.from_env()
    dst = _backup_path(cfg)
    logger.info("Backup destination: %s", dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not dst.parent.exists():
        logger.error("Failed to create backup directory %s", dst.parent)
        raise FileNotFoundError(dst.parent)
    logger.debug("Backup directory exists: %s", dst.parent)
    run_backup(cfg, dst, show_progress=show_progress)
    logger.info("Backup completed: %s", dst)
    return str(dst)

# Cleanup tasks
@actor(queue_name="cleanup", max_retries=1)
def cleanup_old_backups() -> int:
    """Remove backup files older than the configured retention period."""
    cfg = BackupConfig.from_env()
    cutoff = datetime.utcnow() - timedelta(days=cfg.retention_days)
    removed = 0
    backup_dir = Path(cfg.backup_dir)
    for path in backup_dir.glob("*.dump"):
        if path.stat().st_mtime < cutoff.timestamp():
            try:
                path.unlink()
                removed += 1
            except FileNotFoundError:  # pragma: no cover - file might vanish
                continue
    logger.info("Removed %s old backups", removed)
    return removed

# register the actor so `.send()` can use the configured broker
remoulade.declare_actors([run_backup_job, cleanup_old_backups])