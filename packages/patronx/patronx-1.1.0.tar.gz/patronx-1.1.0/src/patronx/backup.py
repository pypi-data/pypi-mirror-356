
import os
import subprocess as sp
import time
from pathlib import Path

import boto3
import psycopg2
from tqdm import tqdm

CHUNK = 1_048_576  # 1 MiB


def _db_size(cfg) -> int | None:
    try:
        conn = psycopg2.connect(
            host=cfg.host, port=cfg.port, user=cfg.user,
            password=cfg.password, dbname=cfg.database, connect_timeout=5
        )
        with conn.cursor() as cur:
            cur.execute("SELECT pg_database_size(%s)", (cfg.database,))
            return int(cur.fetchone()[0])
    except Exception:  # pragma: no cover
        return None
    finally:
        try:
            conn.close()
        except Exception:  # pragma: no cover
            pass


def run_backup(cfg, out: Path, *, show_progress: bool) -> None:
    """
    Stream a pg_dump into *out* while displaying a live progress bar.

    cfg  – patronx.config.BackupConfig
    out  – output file or directory
    """
    size = _db_size(cfg) if show_progress else None
    out.parent.mkdir(parents=True, exist_ok=True)

    cmd = ["pg_dump", "-h", cfg.host, "-p", str(cfg.port), "-U", cfg.user, cfg.database]
    cmd += ["-Fp"]

    env = None
    if cfg.password is not None:
        env = {
            **os.environ,
            "PGPASSWORD": cfg.password,
        }
    proc = sp.Popen(
        cmd, stdout=sp.PIPE, stderr=sp.PIPE, bufsize=CHUNK, env=env
    )

    if proc.stdout is None:  # pragma: no cover
        raise RuntimeError("pg_dump failed to start – no stdout")

    stream = proc.stdout
    bar = tqdm(total=size, unit="B", unit_scale=True, desc="Dumping", disable=not show_progress or size is None)

    start = time.time()
    with out.open("wb") as fh:
        while chunk := stream.read(CHUNK):
            fh.write(chunk)
            bar.update(len(chunk))

    bar.close()
    rc = proc.wait()
    if rc != 0:  # pragma: no cover
        raise RuntimeError(proc.stderr.read().decode())

    if getattr(cfg, "s3_bucket", None):
        key = f"{out}"
        _upload_to_s3(out, cfg.s3_bucket, key)

    elapsed = time.time() - start
    print(f"wrote {out.stat().st_size/1_048_576:,.1f} MiB in {elapsed:,.1f}s "
          f"({out.stat().st_size/elapsed/1_048_576:,.1f} MiB/s)")



def run_restore(cfg, inp: Path, *, show_progress: bool) -> None:
    """Restore a database from *inp* while optionally showing a progress bar."""
    # remove all existing objects to avoid conflicts during restore
    conn = psycopg2.connect(
        host=cfg.host,
        port=cfg.port,
        user=cfg.user,
        password=cfg.password,
        dbname=cfg.database,
    )
    with conn:
        with conn.cursor() as cur:
            cur.execute("DROP SCHEMA IF EXISTS public CASCADE")
            cur.execute("CREATE SCHEMA public")
    conn.close()

    size = inp.stat().st_size if show_progress else None

    cmd = [
        "psql",
        "-h",
        cfg.host,
        "-p",
        str(cfg.port),
        "-U",
        cfg.user,
        cfg.database,
    ]
    env = None
    if cfg.password is not None:
        env = {
            **os.environ,
            "PGPASSWORD": cfg.password,
        }
    proc = sp.Popen(
        cmd, stdin=sp.PIPE, stderr=sp.PIPE, bufsize=CHUNK, env=env
    )
    if proc.stdin is None:  # pragma: no cover
        raise RuntimeError("restore process failed to start – no stdin")

    bar = tqdm(
        total=size,
        unit="B",
        unit_scale=True,
        desc="Restoring",
        disable=not show_progress or size is None,
    )

    start = time.time()
    with inp.open("rb") as fh:
        while chunk := fh.read(CHUNK):
            proc.stdin.write(chunk)
            bar.update(len(chunk))
    proc.stdin.close()

    bar.close()
    rc = proc.wait()
    if rc != 0:  # pragma: no cover
        raise RuntimeError(proc.stderr.read().decode())

    elapsed = time.time() - start
    print("db restored in " + str(elapsed))


def _upload_to_s3(file: Path, bucket: str, key: str) -> None:
    """Upload *file* to ``s3://bucket/key`` using default AWS creds."""
    s3 = boto3.client("s3")
    s3.upload_file(str(file), bucket, key)
    print(f"uploaded → s3://{bucket}/{key}")