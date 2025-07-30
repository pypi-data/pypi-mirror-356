from datetime import datetime, timedelta, timezone

import boto3
import typer
from azure.identity import AzureCliCredential
from azure.mgmt.costmanagement import CostManagementClient


app = typer.Typer(help="Cost management commands")
report_app = typer.Typer(help="Generate cost reports")
app.add_typer(report_app, name="report")


@report_app.command("azure")
def azure_cost(subscription_id: str = typer.Argument(..., help="Azure subscription ID")):
    """Show Azure cost by service for the current month."""
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
