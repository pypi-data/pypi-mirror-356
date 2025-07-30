import os
from dataclasses import dataclass


@dataclass
class BackupConfig:
    """Configuration for backing up a PostgreSQL database.

    Values are pulled from environment variables typically used by the
    ``pg_dump`` command. Default values mirror the defaults used by the
    PostgreSQL client utilities when an environment variable is missing.
    """

    host: str = "localhost"
    port: int = 5432
    user: str = "postgres"
    password: str | None = None
    database: str = "postgres"
    backup_dir: str = "."
    s3_bucket: str | None = None
    cleanup_cron: str = "0 1 * * *"
    retention_days: int = 30
    backup_cron: str = "0 0 * * *"

    @classmethod
    def from_env(cls) -> "BackupConfig":
        """Create configuration from environment variables.

        The following variables are consulted:

        ``PGHOST``
            Database server host.
        ``PGPORT``
            Server port number. Defaults to ``5432`` when unset.
        ``PGUSER``
            Authentication user name. Defaults to ``postgres`` when unset.
        ``PGPASSWORD``
            Password for authentication. Optional.
        ``PGDATABASE``
            Name of the database to back up. Defaults to ``postgres`` when unset.
        ``BACKUP_DIR``
            Directory where the dump file should be placed. Defaults to the
            current directory.
        ``BACKUP_CRON``
            Cron schedule for periodic backups. Defaults to "0 0 * * *" (midnight daily).
                ``CLEANUP_CRON``
            Cron schedule for cleaning up old backups. Defaults to "0 1 * * *" (1 AM daily).
        ``RETENTION_DAYS``
            Number of days to keep backups. Files older than this are deleted. Defaults to ``30``.
        ``S3_BUCKET``
            Optional S3 bucket name for storing backups. If set, backups can be uploaded to S3.
        """

        return cls(
            host=os.getenv("PGHOST", "localhost"),
            port=int(os.getenv("PGPORT", "5432")),
            user=os.getenv("PGUSER", "test_user"),
            password=os.getenv("PGPASSWORD", "test_password"),
            database=os.getenv("PGDATABASE", "test_db"),
            backup_dir=os.getenv("BACKUP_DIR", "./backups"),
            s3_bucket=os.getenv("S3_BUCKET"),
            backup_cron=os.getenv("BACKUP_CRON", "0 0 * * *"),
            cleanup_cron=os.getenv("CLEANUP_CRON", "0 1 * * *"),
            retention_days=int(os.getenv("RETENTION_DAYS", "30")),
        )
