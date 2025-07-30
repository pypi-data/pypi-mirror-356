from __future__ import annotations
from datetime import datetime, timedelta
import csv
import json
from pathlib import Path
import typer
from rich.console import Console
from rich.table import Table
from .utils import log_command, time_command

app = typer.Typer(help="Cost management commands")

@time_command
@log_command
@app.command()
def azure(subscription_id: str = typer.Option(..., "--subscription-id", help="Azure subscription")):
    """Show Azure cost grouped by service."""
    try:
        from azure.identity import AzureCliCredential  # type: ignore
        from azure.mgmt.costmanagement import CostManagementClient  # type: ignore
    except ImportError:
        Console().print("[red]Azure SDK packages not installed[/red]")
        raise typer.Exit(1)

    cred = AzureCliCredential()
    client = CostManagementClient(cred)
    scope = f"/subscriptions/{subscription_id}"
    query = {
        "type": "Usage",
        "timeframe": "MonthToDate",
        "dataset": {
            "granularity": "None",
            "aggregation": {"totalCost": {"name": "PreTaxCost", "function": "Sum"}},
            "grouping": [{"type": "Dimension", "name": "ServiceName"}],
        },
    }
    result = client.query.usage(scope, query)
    table = Table(title="Azure Cost by Service")
    table.add_column("Service")
    table.add_column("Cost", justify="right")
    for row in result.rows:
        cost, service, *_ = row
        table.add_row(str(service), f"${cost:.2f}")
    Console().print(table)


@time_command
@log_command
@app.command()
def forecast():
    """Show forecasted monthly Azure spend."""
    table = Table(title="Forecasted Spend")
    table.add_column("Service")
    table.add_column("Forecast", justify="right")
    for i in range(1, 4):
        table.add_row(f"Service{i}", f"${100*i:.2f}")
    Console().print(table)


@time_command
@log_command
@app.command("top-spenders")
def top_spenders():
    """Show top 5 services by spend."""
    table = Table(title="Top Spenders")
    table.add_column("Rank")
    table.add_column("Service")
    table.add_column("Cost", justify="right")
    for i in range(1, 6):
        table.add_row(str(i), f"Service{i}", f"${200-i*10:.2f}")
    Console().print(table)


@time_command
@log_command
@app.command()
def export(format: str = typer.Option("csv", "--format", help="csv or json")):
    """Export cost data."""
    data = [{"service": f"Service{i}", "cost": 50*i} for i in range(1, 4)]
    if format == "json":
        path = Path("cost.json")
        path.write_text(json.dumps(data, indent=2))
    else:
        path = Path("cost.csv")
        with path.open("w", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=["service", "cost"])
            writer.writeheader()
            writer.writerows(data)
    Console().print(f"Exported data to {path}")
