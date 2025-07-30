from __future__ import annotations
import shutil
import typer
from rich.console import Console
from rich.table import Table
from .utils import log_command, time_command

TOOLS = ["git", "python", "az", "docker"]

app = typer.Typer(help="Check development environment")


@time_command
@log_command
@app.callback(invoke_without_command=True)
def doctor(ctx: typer.Context):
    """Check if common tooling is available."""
    if ctx.invoked_subcommand is not None:
        return
    console = Console()
    table = Table(title="Doctor")
    table.add_column("Tool")
    table.add_column("Status")
    for tool in TOOLS:
        status = "[green]✓" if shutil.which(tool) else "[red]missing"
        table.add_row(tool, status)
    console.print(table)
