from click.testing import CliRunner

from patronx import __version__, cli
from patronx.cli import main


def test_main_prints_message():
    runner = CliRunner()
    result = runner.invoke(main)
    assert result.exit_code == 0
    assert "PatronX CLI invoked" in result.output


def test_cli_version_option():
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.output


def test_version():
    assert __version__ == "1.1.0"


def test_check_db_success(monkeypatch):
    def fake_connect(**kwargs):
        class FakeConn:
            def close(self):
                pass

        return FakeConn()

    monkeypatch.setattr(cli.psycopg2, "connect", fake_connect)

    runner = CliRunner()
    result = runner.invoke(main, ["check-db"])

    assert result.exit_code == 0
    assert "Database connection successful" in result.output


def test_check_db_failure(monkeypatch):
    def fake_connect(**kwargs):
        raise Exception("boom")

    monkeypatch.setattr(cli.psycopg2, "connect", fake_connect)
    monkeypatch.setattr(cli, "start_backup_scheduler", lambda cron: None)
    monkeypatch.setattr(cli, "start_cleanup_scheduler", lambda cron: None)

    runner = CliRunner()
    result = runner.invoke(main, ["check-db"])

    assert result.exit_code == 1
    assert "Database connection failed" in result.output


def test_run_server(monkeypatch):
    def raise_keyboard_interrupt(seconds):
        raise KeyboardInterrupt

    monkeypatch.setattr(cli.time, "sleep", raise_keyboard_interrupt)
    monkeypatch.setattr(cli, "start_backup_scheduler", lambda cron: None)
    monkeypatch.setattr(cli, "start_cleanup_scheduler", lambda cron: None)

    runner = CliRunner()
    result = runner.invoke(main, ["server"])

    assert result.exit_code == 0
    assert "server running" in result.output.lower()

def test_diff_cmd(monkeypatch):
    monkeypatch.setattr(cli, "diff_last_backup", lambda cfg: "diff")
    runner = CliRunner()
    result = runner.invoke(main, ["diff"])
    assert result.exit_code == 0
    assert "diff" in result.output