import os
import shutil
import subprocess
import time

import psycopg2
import pytest

from patronx.backup import run_backup, run_restore
from patronx.config import BackupConfig


def _has_requirements() -> bool:
    return all(
        shutil.which(cmd) is not None
        for cmd in ("docker", "pg_dump", "pg_restore")
    )


@pytest.mark.skipif(not _has_requirements(), reason="Integration requirements not met")
def test_backup_and_restore(tmp_path):
    compose_file = os.path.join(os.path.dirname(__file__), "docker-compose.test.yml")
    subprocess.run(["docker", "compose", "-f", compose_file, "up", "-d"], check=True)
    try:
        # wait for postgres to become ready
        for _ in range(30):
            try:
                conn = psycopg2.connect(
                    host="localhost",
                    port=5432,
                    user="test_user",
                    password="test_password",
                    dbname="test_db",
                )
                conn.close()
                break
            except Exception:
                time.sleep(1)
        else:
            raise RuntimeError("database not ready in time")

        cfg = BackupConfig(
            host="localhost",
            port=5432,
            user="test_user",
            password="test_password",
            database="test_db",
            backup_dir=str(tmp_path),
        )
        backup_file = tmp_path / "dump"

        # add an extra row
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            user="test_user",
            password="test_password",
            dbname="test_db",
        )
        with conn, conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (name, email) VALUES (%s, %s)",
                ("Alice", "alice@example.com"),
            )
        conn.close()

        run_backup(cfg, backup_file, plain=False, show_progress=False)

        run_restore(cfg, backup_file, plain=False, show_progress=False)

        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            user="test_user",
            password="test_password",
            dbname="test_db",
        )
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM users")
            count = cur.fetchone()[0]
        conn.close()
        assert count == 3
    finally:
        subprocess.run(["docker", "compose", "-f", compose_file, "down", "-v"], check=False)