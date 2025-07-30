
from patronx.config import BackupConfig


def test_from_env_uses_defaults(monkeypatch):
    for var in ["PGHOST", "PGPORT", "PGUSER", "PGPASSWORD", "PGDATABASE", "BACKUP_DIR"]:
        monkeypatch.delenv(var, raising=False)

    backup = BackupConfig.from_env()

    assert backup.host == "localhost"
    assert backup.port == 5432
    assert backup.user == "test_user"
    assert backup.password == "test_password"
    assert backup.database == "test_db"
    assert backup.backup_dir == "./backups"


def test_from_env_reads_values(monkeypatch):
    monkeypatch.setenv("PGHOST", "db")
    monkeypatch.setenv("PGPORT", "6543")
    monkeypatch.setenv("PGUSER", "patronx")
    monkeypatch.setenv("PGPASSWORD", "secret")
    monkeypatch.setenv("PGDATABASE", "mydb")
    monkeypatch.setenv("BACKUP_DIR", "/tmp")

    backup = BackupConfig.from_env()

    assert backup.host == "db"
    assert backup.port == 6543
    assert backup.user == "patronx"
    assert backup.password == "secret"
    assert backup.database == "mydb"
    assert backup.backup_dir == "/tmp"
