from __future__ import annotations
import json
from pathlib import Path
import typer
from rich.console import Console
from .utils import log_command, time_command

CONFIG_FILE = Path.home() / ".chatops_config.json"

app = typer.Typer(help="Configuration")


def _load() -> dict:
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text())
        except Exception:
            return {}
    return {}


def _save(data: dict) -> None:
    CONFIG_FILE.write_text(json.dumps(data, indent=2))


@time_command
@log_command
@app.command("set")
def set_value(key: str = typer.Argument(...), value: str = typer.Argument(...)):
    """Set a configuration value."""
    data = _load()
    data[key] = value
    _save(data)
    Console().print(f"Set {key}={value}")


@time_command
@log_command
@app.command("get")
def get_value(key: str = typer.Argument(...)):
    """Get a configuration value."""
    data = _load()
    Console().print(data.get(key, ""))
