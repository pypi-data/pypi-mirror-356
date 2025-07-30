"""ChatOps command line application."""

__version__ = "0.5.0"

from .cli import app
from .suggest import suggest_command

__all__ = ["app", "suggest_command"]
