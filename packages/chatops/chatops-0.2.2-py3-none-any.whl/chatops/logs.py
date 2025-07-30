from __future__ import annotations
import time
import typer
from rich.console import Console
from rich.table import Table
from rich.live import Live
from .utils import log_command, time_command

app = typer.Typer(help="Logging related commands")


@time_command
@log_command
@app.command()
def live(service: str):
    """Simulate live logs for a service."""
    console = Console()
    with Live(refresh_per_second=4) as live:
        for i in range(5):
            live.update(Table().add_column("log").add_row(f"{service} log line {i}"))
            time.sleep(0.5)
    console.print("[green]Streaming ended[/green]")


@time_command
@log_command
@app.command()
def grep(pattern: str):
    """Search mock logs."""
    logs = ["error starting service", "service ready", "warning: high memory"]
    matches = [l for l in logs if pattern in l]
    table = Table(title="Matches")
    table.add_column("Line")
    for m in matches:
        table.add_row(m)
    Console().print(table)


@time_command
@log_command
@app.command()
def tail(service: str, lines: int = typer.Option(50, "--lines")):
    """Tail fake log output."""
    table = Table(title=f"{service} logs")
    table.add_column("Line")
    for i in range(lines):
        table.add_row(f"log line {i}")
    Console().print(table)
