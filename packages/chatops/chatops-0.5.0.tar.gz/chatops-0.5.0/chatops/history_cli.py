from __future__ import annotations
import typer
from rich.console import Console
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
