from __future__ import annotations
import typer
from rich.console import Console
from pathlib import Path
from . import history
from .utils import log_command, time_command

app = typer.Typer(help="Command history")

@time_command
@log_command
@app.command()
def show(limit: int = typer.Option(10, help="Number of entries")):
    """Show recent command history."""
    console = Console()
    for entry in history.recent(limit):
        console.print(f"[cyan]{entry.get('timestamp')}[/cyan] {entry.get('command')}")


@time_command
@log_command
@app.command("usage")
def usage(limit: int = typer.Option(10, help="Number of lines")):
    """Show raw usage log."""
    log_file = Path.home() / ".chatops" / "usage.log"
    console = Console()
    if not log_file.exists():
        console.print("No usage log found")
        return
    lines = log_file.read_text().splitlines()[-limit:]
    for line in lines:
        console.print(line)
