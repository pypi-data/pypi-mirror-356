from functools import wraps
from time import perf_counter
import logging
from datetime import datetime
from click import get_current_context
from pathlib import Path
from . import history

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

USAGE_LOG = Path.home() / ".chatops" / "usage.log"


def log_command(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info("Running %s", func.__name__)
        try:
            ctx = get_current_context(silent=True)
        except Exception:
            ctx = None
        cmd = ctx.command_path if ctx else func.__name__
        timestamp = datetime.utcnow().isoformat()
        history.add_entry({"timestamp": timestamp, "command": cmd})
        try:
            USAGE_LOG.parent.mkdir(parents=True, exist_ok=True)
            with USAGE_LOG.open("a") as fh:
                fh.write(f"{timestamp} {cmd}\n")
        except Exception:  # pragma: no cover - logging errors
            pass
        return func(*args, **kwargs)
    return wrapper


def time_command(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            duration = perf_counter() - start
            logger.info("%s completed in %.2fs", func.__name__, duration)
    return wrapper
