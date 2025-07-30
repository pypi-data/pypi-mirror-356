from __future__ import annotations

import functools
from pathlib import Path
from typing import Callable, TypeVar

import click
from dotenv import load_dotenv

T = TypeVar("T", bound=Callable[..., object])

def load_env_file(path: str | Path) -> None:
    """Load environment variables from *path* if allowed."""
    p = Path(path)
    if not p.exists():
        raise click.ClickException(f"env file '{p}' not found")
    load_dotenv(p)


def env_file_option(func: T) -> T:
    """Add an ``--env-file`` option to *func* and load the file when used."""

    @click.option(
        "--env-file",
        type=click.Path(dir_okay=False, exists=True),
        help="Path to a file containing environment variables (dev only)",
    )
    @functools.wraps(func)
    def wrapper(*args, env_file: str | None = None, **kwargs):
        if env_file:
            load_env_file(env_file)
        return func(*args, **kwargs)

    return wrapper  # type: ignore[misc]