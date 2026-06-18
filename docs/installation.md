# Karakana Installation

## Local Editable Install

Karakana is a Python package with a Typer CLI entrypoint.

```bash
python -m venv .venv
.venv/bin/python -m pip install -e ".[dev]"
.venv/bin/karakana --help
```

When the `karakana` command is already available from an activated environment or another install, `karakana codex start --project <project>` can bootstrap a missing project `.venv` automatically before launching Codex. It runs the same local editable install command shown above. Use `--no-bootstrap` to skip automatic setup.

If `karakana` is not on `PATH` and the project `.venv` does not exist yet, start from the source checkout with Python instead:

```bash
python -m karakana codex start --project <project>
```

That source-tree entrypoint uses the standard library to create `.venv`, installs the local package, and then re-enters Karakana through the new environment.

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
