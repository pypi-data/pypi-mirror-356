## PatronX
_Toolkit for PostgreSQL backups, point‑in‑time recovery (PITR) and object‑storage off‑loading, written in modern‑typed_


<img src="./patronx.png" />

[![codecov](https://codecov.io/gh/xdanielsb/patron/graph/badge.svg?token=AHTJFKDSKU)](https://codecov.io/gh/xdanielsb/patron)
![CI](https://github.com/xdanielsb/patron/actions/workflows/ci-test.yml/badge.svg)
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
```

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
