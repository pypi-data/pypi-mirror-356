from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict

HISTORY_FILE = Path.home() / ".chatops_history.json"


def _load() -> List[Dict]:
    if HISTORY_FILE.exists():
        try:
            return json.loads(HISTORY_FILE.read_text())
        except Exception:
            return []
    return []


def add_entry(entry: Dict) -> None:
    data = _load()
    data.append(entry)
    # keep only last 50 entries
    HISTORY_FILE.write_text(json.dumps(data[-50:], indent=2))


def recent(limit: int = 10) -> List[Dict]:
    return _load()[-limit:]
