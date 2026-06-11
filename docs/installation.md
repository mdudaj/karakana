# Karakana Installation

## Local Editable Install

Karakana is a Python package with a Typer CLI entrypoint.

```bash
python -m venv .venv
.venv/bin/python -m pip install -e ".[dev]"
.venv/bin/karakana --help
```

## Python Version

The package metadata requires Python 3.11 or newer.

## pipx or uv

For isolated CLI use, install with your preferred Python package tool once packaging is ready. During local development, editable install is preferred.

## Validate the Install

```bash
karakana version
karakana doctor
karakana config validate
```

The doctor command is read-only except for writing local reports under `.karakana/doctor/`.
