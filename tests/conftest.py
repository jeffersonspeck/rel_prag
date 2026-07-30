from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from epm.api import app
from epm.audit import AuditLogger
from epm.ontology import OntologyRepository
from epm.policies import PolicyRepository
from epm.service import EpistemicPragmaticService

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture()
def service(tmp_path):
    return EpistemicPragmaticService(
        ontology_repository=OntologyRepository(ROOT / "data"),
        policy_repository=PolicyRepository(ROOT / "data" / "policies"),
        audit_logger=AuditLogger(tmp_path / "audit.jsonl"),
    )


@pytest.fixture()
def client():
    return TestClient(app)
