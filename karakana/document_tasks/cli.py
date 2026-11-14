"""Thin explicit preparation command; no live/check/verify options in S1."""

from enum import Enum
from pathlib import Path

import typer

from .inputs import json_bytes
from .prepare import prepare_task
from .report import render_text


app = typer.Typer(help="Prepare explicit local document tasks. Content checking is separate.")


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
