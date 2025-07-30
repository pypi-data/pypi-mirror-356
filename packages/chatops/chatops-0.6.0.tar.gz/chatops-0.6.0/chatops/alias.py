from __future__ import annotations
import json
from pathlib import Path
import typer
from .utils import log_command, time_command

ALIAS_FILE = Path.home() / ".chatops_aliases.json"

app = typer.Typer(help="Command aliases")


def _load() -> dict:
    if ALIAS_FILE.exists():
        try:
            return json.loads(ALIAS_FILE.read_text())
        except Exception:
            return {}
    return {}


def _save(data: dict) -> None:
    ALIAS_FILE.write_text(json.dumps(data, indent=2))


@time_command
@log_command
@app.command("create")
def create(alias: str = typer.Argument(...), command: str = typer.Argument(...)):
    """Create a command alias."""
    data = _load()
    data[alias] = command
    _save(data)
    typer.echo(f"Alias {alias} -> {command} created")
