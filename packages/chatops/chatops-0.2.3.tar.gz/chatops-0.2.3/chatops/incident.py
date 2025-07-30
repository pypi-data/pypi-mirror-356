from __future__ import annotations
import typer
from rich.console import Console
from rich.table import Table
from .utils import log_command, time_command

app = typer.Typer(help="Incident management commands")
report_app = typer.Typer(help="Incident report commands")
app.add_typer(report_app, name="report")


@time_command
@log_command
@app.command("ack")
def ack(incident_id: str):
    """Acknowledge a fake incident."""
    Console().print(f"Incident {incident_id} acknowledged")


@time_command
@log_command
@app.command("who")
def who():
    """Show on-call rotation list."""
    table = Table(title="On Call")
    table.add_column("Name")
    table.add_row("Alice")
    table.add_row("Bob")
    Console().print(table)


@time_command
@log_command
@app.command("runbook")
def runbook(topic: str):
    """Print SOP for a topic."""
    Console().print(f"Runbook for {topic}: reboot server then retry")


@time_command
@log_command
@report_app.command("create")
def report_create():
    """Generate postmortem template."""
    Console().print("# Postmortem Template\n- what happened\n- impact\n- action items")
