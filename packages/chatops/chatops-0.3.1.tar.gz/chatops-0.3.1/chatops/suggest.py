import os
from pathlib import Path
from typing import List, Tuple

import numpy as np
import openai
from datetime import datetime
from .openai_utils import ensure_api_key
from . import history
import typer
from rich.console import Console


# Known CLI commands and a short description for embedding purposes
_COMMANDS: List[Tuple[str, str]] = [
    ("deploy deploy APP ENV", "Deploy the given app to the specified environment"),
    ("deploy status", "Show deployment status"),
    ("deploy rollback APP ENV", "Rollback to the last successful deployment"),
    ("logs show", "Show recent log entries"),
    (
        "cost report azure SUBSCRIPTION_ID",
        "Show Azure cost by service for the current month",
    ),
    ("incident list", "List current incidents"),
    ("security scan", "Run security scan"),
]

# Cache for command embeddings
_COMMAND_EMBEDDINGS: List[Tuple[str, np.ndarray]] | None = None

app = typer.Typer(help="AI helper commands")


def _get_client() -> openai.OpenAI:
    """Return an OpenAI client after ensuring an API key is available."""
    ensure_api_key()
    return openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def _embed(text: str, client: openai.OpenAI) -> np.ndarray:
    """Return the embedding vector for the given text."""
    response = client.embeddings.create(model="text-embedding-3-small", input=[text])
    return np.array(response.data[0].embedding, dtype=float)


def _load_command_embeddings(client: openai.OpenAI) -> List[Tuple[str, np.ndarray]]:
    """Compute and cache embeddings for known commands."""
    global _COMMAND_EMBEDDINGS
    if _COMMAND_EMBEDDINGS is None:
        _COMMAND_EMBEDDINGS = []
        for cmd, desc in _COMMANDS:
            _COMMAND_EMBEDDINGS.append((cmd, _embed(desc, client)))
    return _COMMAND_EMBEDDINGS


def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def suggest_command(user_query: str) -> str:
    """Return the CLI command that best matches the plain English query.

    Parameters
    ----------
    user_query: str
        A natural language request like ``"restart app on prod"``.

    Returns
    -------
    str
        The closest matching CLI command string.
    """
    client = _get_client()
    files_context = []
    for name in ["Dockerfile", "main.tf", ".env", "pyproject.toml"]:
        p = Path.cwd() / name
        if p.exists():
            try:
                files_context.append(p.read_text()[:500])
            except Exception:
                pass
    hist = history.recent(6)
    hist_text = "\n".join(item.get("content", "") for item in hist if item.get("role") == "user")
    query_text = user_query + "\n" + "\n".join(files_context) + "\n" + hist_text
    query_emb = _embed(query_text, client)
    commands = _load_command_embeddings(client)

    best_cmd = max(commands, key=lambda pair: _cosine_similarity(query_emb, pair[1]))
    return best_cmd[0]

import typer
from rich.console import Console
from .utils import log_command, time_command


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context, prompt: str = typer.Argument(None, help="Prompt")):
    """Suggest a command when no subcommand is given."""
    if ctx.invoked_subcommand is None:
        if not prompt:
            typer.echo("Provide PROMPT or see --help")
            raise typer.Exit(1)
        suggest(prompt)


@time_command
@log_command
@app.command()
def suggest(prompt: str = typer.Argument(..., help="Prompt to analyze")):
    """Suggest best ChatOps command."""
    history.add_entry({"timestamp": datetime.utcnow().isoformat(), "role": "user", "content": prompt})
    try:
        cmd = suggest_command(prompt)
    except Exception as exc:
        Console().print(f"Error: {exc}")
        raise typer.Exit(1)
    Console().print(cmd)
    history.add_entry({"timestamp": datetime.utcnow().isoformat(), "role": "assistant", "content": cmd})


@time_command
@log_command
@app.command()
def explain(text: str = typer.Argument(..., help="Error message")):
    """Use OpenAI to explain an error message."""
    try:
        client = _get_client()
        resp = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": text}])
        Console().print(resp.choices[0].message.content)
    except Exception as exc:
        Console().print(f"OpenAI error: {exc}")
        raise typer.Exit(1)

