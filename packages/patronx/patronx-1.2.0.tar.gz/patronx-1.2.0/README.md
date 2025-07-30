# PatronX

PatronX is a lightweight toolkit for PostgreSQL backups, point‑in‑time recovery
and object‑storage offloading. The project is written in modern typed Python
and ships with a clean command‑line interface.

<img src="./patronx.jpg" width="200" />

[![codecov](https://codecov.io/gh/xdanielsb/patron/graph/badge.svg?token=AHTJFKDSKU)](https://codecov.io/gh/xdanielsb/patron)
![Test](https://github.com/xdanielsb/patron/actions/workflows/ci-test.yml/badge.svg)
![Docker publish](https://github.com/xdanielsb/patronx/actions/workflows/cd-docker-publish.yml/badge.svg)
![PyPI publish](https://github.com/xdanielsb/patronx/actions/workflows/cd-publish-to-pypi.yml/badge.svg)
[![PyPI](https://img.shields.io/pypi/v/patronx)](https://pypi.org/project/patronx/)

## Features

- Simple CLI for backup, restore and listing available dumps
- Scheduled backups via cron expressions
- Optional upload to S3 for off‑site storage
- Typed Python code with unit tests

## DB
- postgres >= 16

```bash
pip install -e . # to install in editable mode
patronx --version
patronx list
patronx check-db
patronx backup [--plain] [--no-progress]
patronx restore --inp /path/to/backup.dump [--plain] [--no-progress]
patronx server

patronx enqueue-backup # with remoulade and rabbitmq
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
