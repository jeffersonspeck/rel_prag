"""Runtime settings with environment-variable overrides."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Settings:
    data_dir: Path
    audit_path: Path
    host: str
    port: int


def get_settings() -> Settings:
    data_dir = Path(os.getenv("EPM_DATA_DIR", PROJECT_ROOT / "data")).resolve()
    audit_path = Path(os.getenv("EPM_AUDIT_PATH", PROJECT_ROOT / "output" / "audit.jsonl")).resolve()
    return Settings(
        data_dir=data_dir,
        audit_path=audit_path,
        host=os.getenv("EPM_HOST", "127.0.0.1"),
        port=int(os.getenv("EPM_PORT", "8000")),
    )
