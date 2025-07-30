from __future__ import annotations
import random
import typer
from rich.console import Console
from rich.table import Table
from .utils import log_command, time_command

app = typer.Typer(help="Metrics commands")


@time_command
@log_command
@app.command("latency")
def latency(service: str = typer.Option(..., "--service", help="Service name")):
    """Simulate fetching latency metrics."""
    console = Console()
    table = Table(title=f"Latency for {service}")
    table.add_column("Percentile")
    table.add_column("ms")
    for p in ["p50", "p95", "p99"]:
        table.add_row(p, str(random.randint(10, 200)))
    console.print(table)
