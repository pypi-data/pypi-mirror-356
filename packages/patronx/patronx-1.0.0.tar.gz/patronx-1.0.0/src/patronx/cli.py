import time
from pathlib import Path

import click
import psycopg2


from patronx.tasks import run_backup_job
from patronx.schedule import start_backup_scheduler
from patronx.schedule import start_cleanup_scheduler
from patronx.tasks import cleanup_old_backups

from . import __version__
from .backup import run_backup, run_restore
from .config import BackupConfig


@click.group(invoke_without_command=True)
@click.version_option(version=__version__)
@click.pass_context
def main(ctx: click.Context) -> None:
    """Entry point for the :command:`patronx` command."""
    if ctx.invoked_subcommand is None:
        click.echo("PatronX CLI invoked")


@main.command("check-db")
def check_db() -> None:
    """Check connection to the configured database."""
    cfg = BackupConfig.from_env()
    try:
        conn = psycopg2.connect(
            host=cfg.host,
            port=cfg.port,
            user=cfg.user,
            password=cfg.password,
            dbname=cfg.database,
            connect_timeout=5,
        )
        conn.close()
        click.echo("Database connection successful")
    except Exception as exc:  # pragma: no cover - connection can fail
        raise click.ClickException(f"Database connection failed: {exc}") from exc


@main.command("backup")
@click.option("--plain", is_flag=True, help="Dump as plain SQL instead of PostgreSQL custom format")
@click.option("--no-progress", is_flag=True, help="Turn off progress bar (useful in CI)")
def backup_cmd(plain, no_progress):
    cfg = BackupConfig.from_env()
    ts = time.strftime("%Y%m%dT%H%M%S")
    suffix = "sql.gz" if plain else "dump"
    out = Path(f"{cfg.backup_dir}/{cfg.database}_{ts}.{suffix}")

    run_backup(
        cfg,
        out,
        plain=plain,
        show_progress=not no_progress,
    )


@main.command("restore")
@click.option("--inp", required=True, help="Path of the backup file to restore from")
@click.option("--plain", is_flag=True, help="Dump as plain SQL instead of PostgreSQL custom format")
@click.option("--no-progress", is_flag=True, help="Turn off progress bar (useful in CI)")
def restore_cmd(inp, plain, no_progress):
    cfg = BackupConfig.from_env()
    inp_path = Path(inp)
    run_restore(
        cfg,
        inp_path,
        plain=plain,
        show_progress=not no_progress,
    )


@main.command(name="list")
def list_backups() -> None:
    """List all backups in the configured backup directory."""
    config = BackupConfig.from_env()
    path = Path(config.backup_dir)

    if not path.exists():
        click.echo(f"Backup directory {path} does not exist")
        return

    for backup in sorted(p for p in path.iterdir() if p.is_file()):
        click.echo(backup.name)


@main.command()
def server() -> None:
    """Run a server that schedules periodic backups and cleanup."""

    config = BackupConfig.from_env()
    start_backup_scheduler(config.backup_cron)
    start_cleanup_scheduler(config.cleanup_cron)
    click.echo("PatronX server running. Press Ctrl+C to exit")
    try:
        while True:  # pragma: no cover - loop is terminated in tests
            time.sleep(1)
    except KeyboardInterrupt:  # pragma: no cover - user exit
        pass

@main.command("enqueue-backup")
def enqueue_backup():
    """Fire an ad-hoc backup job right now."""
    click.echo(run_backup_job.send())


@main.command("enqueue-cleanup")
def enqueue_cleanup() -> None:
    """Fire an ad-hoc cleanup job right now."""
    click.echo(cleanup_old_backups.send())