# Karakana Known Issues

Track known defects, limitations, stale assumptions, and implementation risks that should be considered during future work.

- The repository-local Karakana CLI may not have a generated `.venv/bin/karakana` console script even when `.venv`, `karakana/cli.py`, and dependencies such as Typer exist. Do not assume `karakana` is on `PATH`, and do not treat `python -m karakana.cli` as equivalent because the module exposes a Typer `app` but does not call it under `__main__`. If the console script is missing and editable install is unavailable, invoke commands from the repository root with `.venv/bin/python -c "from karakana.cli import app; app()" <args>`, for example `.venv/bin/python -c "from karakana.cli import app; app()" handoff load --project crdb-mel --skillpack crdb-mel`.
