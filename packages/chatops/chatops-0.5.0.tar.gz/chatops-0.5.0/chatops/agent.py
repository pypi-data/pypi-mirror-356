from __future__ import annotations
import time
import random
import typer
from rich.console import Console
from .utils import log_command, time_command

app = typer.Typer(help="Autonomous agent")


@time_command
@log_command
@app.command("run")
def run(condition: str = typer.Argument(..., help="Condition -> action"), dry_run: bool = typer.Option(False, "--dry-run")):
    """Run autonomous agent with polling."""
    console = Console()
    console.print(f"Evaluating rule: {condition}")
    if "->" not in condition:
        console.print("[red]Condition must be in 'if ... -> action' form[/red]")
        raise typer.Exit(1)
    check, action = [c.strip() for c in condition.split("->", 1)]
    console.print(f"Will execute '{action}' when '{check}' is met")
    try:
        for _ in range(5):
            time.sleep(1)
            metric = random.randint(50, 100)
            console.print(f"CPU usage: {metric}%")
            if metric > 80:
                console.print(f"Condition met at {metric}%")
                if not dry_run:
                    console.print(f"[green]Executing: {action}[/green]")
                else:
                    console.print("[yellow]Dry run - no action taken[/yellow]")
                break
        else:
            console.print("Condition not met during polling window")
    except KeyboardInterrupt:
        console.print("[red]Agent stopped[/red]")
