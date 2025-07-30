from __future__ import annotations
import os
import subprocess
import typer
from rich.console import Console
from rich.table import Table
from .utils import log_command, time_command
from . import env as env_mod

app = typer.Typer(help="Cloud provider utilities")


@app.command()
@time_command
@log_command
def whoami(
    ctx: typer.Context,
    provider: str = typer.Option(None, "--provider", help="aws|azure|gcp"),
):
    """Show identity information for the given cloud provider."""
    console = Console()
    if provider is None:
        env_cfg = env_mod.get_env(ctx.obj.get("env_override"))
        if not env_cfg:
            console.print("[red]No active environment[/red]")
            raise typer.Exit(1)
        provider = env_cfg.get("provider")
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
def top_services(
    ctx: typer.Context,
    provider: str = typer.Option(None, "--provider", help="aws|azure|gcp"),
):
    """Show top services by cost."""
    if provider is None:
        env_cfg = env_mod.get_env(ctx.obj.get("env_override"))
        if not env_cfg:
            Console().print("[red]No active environment[/red]")
            raise typer.Exit(1)
        provider = env_cfg.get("provider")
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
    ctx: typer.Context,
    service: str = typer.Option(..., "--service", help="Service name"),
    region: str = typer.Option("us-east-1", "--region", help="Target region"),
    provider: str = typer.Option(None, "--provider", help="aws|azure|gcp"),
):
    """Simulate deploying a cloud service."""
    if provider is None:
        env_cfg = env_mod.get_env(ctx.obj.get("env_override"))
        if not env_cfg:
            Console().print("[red]No active environment[/red]")
            raise typer.Exit(1)
        provider = env_cfg.get("provider")
    Console().print(f"Deploying {service} to {provider} in {region}...")

