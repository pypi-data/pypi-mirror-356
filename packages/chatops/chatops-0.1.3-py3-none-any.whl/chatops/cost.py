from datetime import datetime, timedelta, timezone

import typer

from rich.console import Console
from rich.table import Table


app = typer.Typer(help="Cost management commands")
report_app = typer.Typer(help="Generate cost reports")
app.add_typer(report_app, name="report")


@report_app.command("azure")
def azure_cost(subscription_id: str = typer.Argument(..., help="Azure subscription ID")):
    """Show Azure cost by service for the current month."""
    try:
        from azure.identity import AzureCliCredential  # type: ignore
        from azure.mgmt.costmanagement import CostManagementClient  # type: ignore
    except ImportError:
        typer.echo("Azure SDK packages are required for this command")
        raise typer.Exit(code=1)

    credential = AzureCliCredential()
    client = CostManagementClient(credential)
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

    table = Table(title="Azure Cost by Service (Month To Date)")
    table.add_column("Service", style="cyan")
    table.add_column("Cost", justify="right")

    for row in result.rows:
        service, cost = row
        table.add_row(str(service), f"${cost:.2f}")


    Console().print(table)
