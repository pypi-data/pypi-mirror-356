from __future__ import annotations
import json
from pathlib import Path
import typer
from rich.console import Console
from .utils import log_command, time_command

FEEDBACK_FILE = Path.home() / ".chatops_feedback.json"

app = typer.Typer(help="User feedback")


def _load() -> list:
    if FEEDBACK_FILE.exists():
        try:
            return json.loads(FEEDBACK_FILE.read_text())
        except Exception:
            return []
    return []


def _save(data: list) -> None:
    FEEDBACK_FILE.write_text(json.dumps(data, indent=2))


@time_command
@log_command
@app.command()
def rate(last: bool = typer.Option(False, "--last", help="Rate last response"), rate: str = typer.Argument(..., help="up or down")):
    """Rate model response quality."""
    data = _load()
    entry = {"timestamp": str(Path().stat().st_mtime), "rate": rate, "last": last}
    data.append(entry)
    _save(data)
    Console().print(f"Recorded feedback: {rate}")
