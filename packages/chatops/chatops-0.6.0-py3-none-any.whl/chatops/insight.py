from __future__ import annotations
import typer
from rich.console import Console
from rich.table import Table
from datetime import datetime, timedelta
from .utils import log_command, time_command

app = typer.Typer(help="Observability insights")


@time_command
@log_command
@app.command("top-errors")
def top_errors(window: str = typer.Option("1h", "--window", help="Time window")):
    """Show top errors for the time window."""
    console = Console()
    table = Table(title=f"Top errors last {window}")
    table.add_column("Timestamp")
    table.add_column("Error")
    now = datetime.utcnow()
    for i in range(3):
        ts = now - timedelta(minutes=i * 10)
        table.add_row(ts.isoformat(), f"Error {i}")
    console.print(table)
