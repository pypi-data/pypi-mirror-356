from rich.console import Console
from rich.syntax import Syntax
import typer

from rich.table import Table

app = typer.Typer(help="Logging related commands")

@app.command()
def show(tail: int = 10):
    """Show recent logs."""
    typer.echo(f"Showing last {tail} log entries")

@app.command("aws")
def aws_logs(
    service: str = typer.Argument(..., help="Service identifier"),
    log_group: str = typer.Option(None, "--log-group", "-g", help="CloudWatch log group"),
    log_stream: str = typer.Option(
        None, "--log-stream", "-s", help="CloudWatch log stream"
    ),
):
    """Fetch the latest 50 log events from AWS CloudWatch Logs."""

    try:
        import boto3  # type: ignore
    except ImportError:
        typer.echo("boto3 is required for this command")
        raise typer.Exit(code=1)

    if not log_group:
        log_group = typer.prompt("Log group name")
    if not log_stream:
        log_stream = typer.prompt("Log stream name")

    client = boto3.client("logs")
    response = client.get_log_events(
        logGroupName=log_group,
        logStreamName=log_stream,
        limit=50,
        startFromHead=False,
    )

    console = Console()
    console.print(f"[bold]Service:[/] {service}")
    for event in response.get("events", []):
        console.print(Syntax(event.get("message", ""), "bash", theme="ansi_dark"))
