"""Append-only JSONL audit trail for policy-based decisions."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Any
from uuid import uuid4


class AuditLogger:
    def __init__(self, path: Path) -> None:
        self.path = path
        self._lock = Lock()

    def record(self, event_type: str, payload: dict[str, Any]) -> str:
        event_id = str(uuid4())
        event = {
            "event_id": event_id,
            "event_type": event_type,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "payload": payload,
        }
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._lock:
            with self.path.open("a", encoding="utf-8") as stream:
                stream.write(json.dumps(event, ensure_ascii=False, default=str) + "\n")
        return event_id
