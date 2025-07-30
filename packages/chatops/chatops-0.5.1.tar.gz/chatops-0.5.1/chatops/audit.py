from __future__ import annotations
import typer
from rich.console import Console
from rich.table import Table
from .utils import log_command, time_command

app = typer.Typer(help="Audit commands")


@time_command
@log_command
@app.command("iam")
def audit_iam():
    """Review IAM permissions."""
    table = Table(title="IAM Audit")
    table.add_column("Issue")
    table.add_row("Excessive admin policy")
    table.add_row("Expired role token")
    Console().print(table)
