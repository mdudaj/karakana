"""Explicit local preparation, checking and saved-bundle verification."""

from enum import Enum
from pathlib import Path

import typer

from .inputs import json_bytes
from .prepare import prepare_task
from . import check_task, verify_task
from .report import render_text


app = typer.Typer(help="Prepare, check or verify explicit local document tasks. Review remains required.")


class OutputFormat(str, Enum):
    text = "text"
    json = "json"


@app.command("prepare")
def prepare(
    request: Path = typer.Option(..., "--request", help="Root-relative task request0.1 JSON."),
    root: Path = typer.Option(Path("."), "--root", help="Declared local input/output root."),
    format: OutputFormat = typer.Option(OutputFormat.text, "--format", help="Text summary or clean JSON result."),
    output: Path | None = typer.Option(None, "--output", help="Fresh output directory under .karakana/."),
) -> None:
    """Prepare a captured prompt and new result bundle without checking content or running a model."""
    result = prepare_task(root, request, output)
    typer.echo(json_bytes(result).decode("utf-8") if format == OutputFormat.json else render_text(result), nl=False)
    if result["outcome"] != "prepared":
        raise typer.Exit(code=2)


def _emit(result, format):
    typer.echo(json_bytes(result).decode("utf-8") if format == OutputFormat.json else render_text(result), nl=False)
    if result["outcome"] not in {"checked", "verified"}:
        raise typer.Exit(code=2)


@app.command("check")
def check(
    request: Path = typer.Option(..., "--request", help="Root-relative task request0.1 JSON with explicit check context."),
    root: Path = typer.Option(Path("."), "--root", help="Declared local input/output root."),
    format: OutputFormat = typer.Option(OutputFormat.text, "--format", help="Text summary or clean JSON result."),
    output: Path | None = typer.Option(None, "--output", help="Fresh output directory under .karakana/."),
) -> None:
    """Check declared narrative content into a fresh report/result bundle; do not accept it."""
    _emit(check_task(root, request, output), format)


@app.command("verify")
def verify(
    request: Path = typer.Option(..., "--request", help="Root-relative current task request0.1 JSON."),
    bundle: Path = typer.Option(..., "--bundle", help="Root-relative saved assessment directory under .karakana/."),
    root: Path = typer.Option(Path("."), "--root", help="Declared local input/output root."),
    format: OutputFormat = typer.Option(OutputFormat.text, "--format", help="Text summary or clean JSON result."),
    output: Path | None = typer.Option(None, "--output", help="Fresh verification directory under .karakana/."),
) -> None:
    """Recompute saved content and task provenance into a new bundle; do not infer acceptance."""
    _emit(verify_task(root, request, bundle, output), format)
