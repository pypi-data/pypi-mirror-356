from __future__ import annotations
import time
import requests
import typer
from rich.console import Console
from .utils import log_command, time_command

app = typer.Typer(help="Monitoring commands")


@time_command
@log_command
@app.command("uptime")
def uptime(url: str = typer.Argument(..., help="URL to check")):
    """Perform HTTP health check and response time."""
    start = time.perf_counter()
    try:
        resp = requests.get(url, timeout=5)
        status = resp.status_code
    except Exception as exc:
        Console().print(f"Request failed: {exc}")
        raise typer.Exit(1)
    duration = (time.perf_counter() - start) * 1000
    Console().print(f"{url} responded with {status} in {duration:.1f} ms")


@time_command
@log_command
@app.command("latency")
def latency(threshold: str = typer.Option("300ms", "--threshold", help="Alert threshold")):
    """Simulate latency alert."""
    ms = int(threshold.rstrip("ms"))
    measured = 250
    if measured > ms:
        Console().print(f"[red]Latency {measured}ms exceeds {ms}ms[/red]")
    else:
        Console().print(f"Latency {measured}ms below threshold")
