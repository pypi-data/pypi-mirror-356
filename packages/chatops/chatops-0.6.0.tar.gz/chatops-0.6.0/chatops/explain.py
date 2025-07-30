from __future__ import annotations
import os
import typer
from rich.console import Console
from .utils import log_command, time_command
from .openai_utils import ensure_api_key

try:
    import openai
except Exception:  # pragma: no cover - optional
    openai = None

app = typer.Typer(help="AI assistance")


def _client() -> 'openai.OpenAI':
    if openai is None:
        raise RuntimeError("openai package not installed")
    ensure_api_key()
    return openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])


@time_command
@log_command
@app.command()
def explain(text: str = typer.Argument(..., help="Traceback or error")):
    """Use OpenAI to explain a stack trace."""
    try:
        client = _client()
        resp = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": text}])
        Console().print(resp.choices[0].message.content)
    except Exception as exc:
        Console().print(f"OpenAI error: {exc}")
        raise typer.Exit(1)


@time_command
@log_command
@app.command()
def autofix(file: str = typer.Argument(..., help="File to analyze")):
    """Suggest code improvements."""
    content = open(file).read()
    try:
        client = _client()
        resp = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"Improve this code:\n{content}"}])
        Console().print(resp.choices[0].message.content)
    except Exception as exc:
        Console().print(f"OpenAI error: {exc}")
        raise typer.Exit(1)
