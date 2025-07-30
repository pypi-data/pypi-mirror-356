from __future__ import annotations
import typer
from rich.console import Console
from rich.table import Table
from .utils import log_command, time_command

app = typer.Typer(help="Compliance scanning")


@time_command
@log_command
@app.command("scan")
def scan(profile: str = typer.Option("cmmc", "--profile", help="Compliance profile")):
    """Simulate compliance scan."""
    console = Console()
    table = Table(title=f"{profile.upper()} Scan")
    table.add_column("Check")
    table.add_column("Status")
    checks = ["IAM", "Networking", "Storage"]
    for c in checks:
        table.add_row(c, "PASS")
    console.print(table)
