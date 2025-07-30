from __future__ import annotations
import os
import subprocess
import typer
from rich.console import Console
from rich.table import Table
from .utils import log_command, time_command

app = typer.Typer(help="Cloud provider utilities")


@app.command()
@time_command
@log_command
def whoami(provider: str = typer.Option("aws", "--provider", help="aws|azure|gcp")):
    """Show identity information for the given cloud provider."""
    console = Console()
    if provider == "aws":
        key = os.environ.get("AWS_ACCESS_KEY_ID")
        if key:
            console.print(f"AWS access key: {key}")
        else:
            console.print("[red]AWS credentials not found[/red]")
    elif provider == "azure":
        try:
            result = subprocess.check_output(["az", "account", "show", "--query", "user.name", "-o", "tsv"], text=True)
            console.print(f"Azure user: {result.strip()}")
        except Exception:
            console.print("[red]Azure CLI credentials not found[/red]")
    elif provider == "gcp":
        try:
            result = subprocess.check_output(["gcloud", "config", "get-value", "account"], text=True)
            console.print(f"GCP account: {result.strip()}")
        except Exception:
            console.print("[red]GCP credentials not found[/red]")
    else:
        console.print("[red]Unknown provider[/red]")


cost_app = typer.Typer(help="Cost commands")
app.add_typer(cost_app, name="cost")


@cost_app.command("top-services")
@time_command
@log_command
def top_services(provider: str = typer.Option("aws", "--provider", help="aws|azure|gcp")):
    """Show top services by cost."""
    table = Table(title="Top Services")
    table.add_column("Service")
    table.add_column("Cost", justify="right")
    for i in range(1, 4):
        table.add_row(f"Service{i}", f"${100*i:.2f}")
    Console().print(table)


@app.command()
@time_command
@log_command
def deploy(
    service: str = typer.Option(..., "--service", help="Service name"),
    region: str = typer.Option("us-east-1", "--region", help="Target region"),
    provider: str = typer.Option("aws", "--provider", help="aws|azure|gcp"),
):
    """Simulate deploying a cloud service."""
    Console().print(f"Deploying {service} to {provider} in {region}...")
