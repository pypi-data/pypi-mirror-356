## PatronX
_Toolkit for PostgreSQL backups, point‑in‑time recovery (PITR) and object‑storage off‑loading, written in modern‑typed_


<center><img src="./patronx.jpg" width="200" /></center> 

[![codecov](https://codecov.io/gh/xdanielsb/patron/graph/badge.svg?token=AHTJFKDSKU)](https://codecov.io/gh/xdanielsb/patron)
![CI](https://github.com/xdanielsb/patron/actions/workflows/ci-test.yml/badge.svg)
![Docker](https://github.com/xdanielsb/patronx/actions/workflows/cd-docker-publish.yml/badge.svg)
[![PyPI](https://img.shields.io/pypi/v/patronx)](https://pypi.org/project/patronx/)
### Command line usage

Install the package in editable mode:

```bash
pip install -e .
```

Once installed, the `patron` command becomes available:

```bash
patronx --version
patronx list
patronx check-db
patronx backup [--plain] [--no-progress]
patronx restore --inp /path/to/backup.dump [--plain] [--no-progress]
patronx server
```

The server command starts schedulers that enqueue backup and cleanup jobs
periodically. The backup schedule is controlled via the ``BACKUP_CRON``
environment variable while cleanup uses ``CLEANUP_CRON``. Both take standard
cron expressions. When unset they default to running once per day for backups
and at 1AM for cleanup. Old backups are removed according to the number of days
specified in ``RETENTION_DAYS`` (defaults to ``30``).

### Test
```bash
pytest
```

### Linting and Formatting
```bash
ruff check . --fix
isort .
```


### Generate requirements
```bash
pip install pip-tools
pip-compile --output-file=requirements.txt pyproject.toml
```
