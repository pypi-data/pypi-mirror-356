from __future__ import annotations
import subprocess
from pathlib import Path
import typer
from rich.console import Console
from .openai_utils import openai_client
from .utils import log_command, time_command

app = typer.Typer(help="Testing utilities")


@time_command
@log_command
@app.command("write")
def write_tests(file: Path = typer.Option(..., "--file", exists=True, help="Source file")):
    """Generate tests for a Python file."""
    console = Console()
    try:
        client = openai_client(console)
    except Exception as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(1)
    prompt = f"Write Pytest tests for the following code:\n{file.read_text()[:1000]}"
    resp = client.chat.completions.create(
        model="gpt-4", messages=[{"role": "user", "content": prompt}], stream=True
    )
    parts: list[str] = []
    if hasattr(resp, "__iter__"):
        for chunk in resp:
            delta = chunk.choices[0].delta.content
            if delta:
                console.print(delta, end="")
                parts.append(delta)
        console.print()
    content = "".join(parts)
    test_file = Path(f"test_{file.stem}.py")
    test_file.write_text(content)
    console.print(f"[green]Wrote {test_file}")


@time_command
@log_command
@app.command("run")
def run_tests():
    """Run tests and show summary."""
    console = Console()
    result = subprocess.run(["pytest", "-q"], capture_output=True, text=True)
    console.print(result.stdout)
    if result.returncode == 0:
        console.print("[green]All tests passed[/green]")
    else:
        console.print("[red]Tests failed[/red]")
    raise typer.Exit(result.returncode)
