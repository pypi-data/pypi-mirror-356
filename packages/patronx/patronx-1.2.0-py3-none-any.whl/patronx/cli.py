import time
from pathlib import Path

import click
import psycopg2


from patronx.schedule import start_backup_scheduler, start_cleanup_scheduler
from patronx.tasks import cleanup_old_backups, run_backup_job

from . import __version__
from .backup import run_backup, run_restore, diff_last_backup
from .config import BackupConfig
from .env import env_file_option


@click.group(invoke_without_command=True)
@click.version_option(version=__version__)
@click.pass_context
def main(ctx: click.Context) -> None:
    """Entry point for the :command:`patronx` command."""
    if ctx.invoked_subcommand is None:
        click.echo("PatronX CLI invoked")


@main.command("check-db")
@env_file_option
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
@env_file_option
@click.option("--no-progress", is_flag=True, help="Turn off progress bar (useful in CI)")
def backup_cmd(no_progress):
    cfg = BackupConfig.from_env()
    ts = time.strftime("%Y%m%dT%H%M%S")
    suffix = "dump"
    out = Path(f"{cfg.backup_dir}/{cfg.database}_{ts}.{suffix}")

    run_backup(
        cfg,
        out,
        show_progress=not no_progress,
    )


@main.command("restore")
@env_file_option
@click.option("--inp", required=True, help="Path of the backup file to restore from")
@click.option("--no-progress", is_flag=True, help="Turn off progress bar (useful in CI)")
def restore_cmd(inp, no_progress):
    cfg = BackupConfig.from_env()
    inp_path = Path(inp)
    run_restore(
        cfg,
        inp_path,
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

    backups = sorted(p for p in path.iterdir() if p.is_file())

    if not backups:
        click.echo("No backups found")
        return

    entries = [
        (
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(b.stat().st_mtime)),
            b.name,
        )
        for b in backups
    ]

    date_width = max(len(r[0]) for r in entries + [("DATE", "NAME")])
    name_width = max(len(r[1]) for r in entries + [("DATE", "NAME")])
    fmt = f"{{:<{date_width}}}  {{:<{name_width}}}"

    click.echo(fmt.format("DATE", "NAME"))
    click.echo("-" * date_width + "  " + "-" * name_width)
    for row in entries:
        click.echo(fmt.format(*row))

@main.command()
@env_file_option
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
@env_file_option
def enqueue_backup():
    """Fire an ad-hoc backup job right now."""
    click.echo(run_backup_job.send())


@main.command("enqueue-cleanup")
@env_file_option
def enqueue_cleanup() -> None:
    """Fire an ad-hoc cleanup job right now."""
    click.echo(cleanup_old_backups.send())


@main.command("diff")
@env_file_option
def diff_cmd() -> None:
    """Diff the latest backup against the current database."""
    cfg = BackupConfig.from_env()
    try:
        output = diff_last_backup(cfg)
        click.echo(output)
    except FileNotFoundError as exc:  # pragma: no cover - no backups yet
        raise click.ClickException(str(exc)) from exc