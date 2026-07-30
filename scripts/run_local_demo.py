"""Run the two independent system scenarios without starting HTTP."""

from __future__ import annotations

import json
from pathlib import Path

from epm.audit import AuditLogger
from epm.models import RelevanceRequest, SimilarityRequest
from epm.ontology import OntologyRepository
from epm.policies import PolicyRepository
from epm.service import EpistemicPragmaticService

ROOT = Path(__file__).resolve().parents[1]


def build_service() -> EpistemicPragmaticService:
    return EpistemicPragmaticService(
        ontology_repository=OntologyRepository(ROOT / "data"),
        policy_repository=PolicyRepository(ROOT / "data" / "policies"),
        audit_logger=AuditLogger(ROOT / "output" / "audit.jsonl"),
    )


def main() -> None:
    service = build_service()
    state = {
        "p_material": 0.2,
        "p_structure": 1.0,
        "p_float": 1.0,
        "p_origin": 1.0,
        "p_historical_value": 0.8,
        "p_monument_role": 1.0,
    }

    navigation = service.relevance(
        RelevanceRequest(
            policy_id="navigation-v1",
            descriptor_values=state,
            aggregator="weighted_average",
        )
    )
    preservation = service.relevance(
        RelevanceRequest(
            policy_id="preservation-v1",
            descriptor_values=state,
            aggregator="weighted_average",
        )
    )

    left = state
    right = {
        "p_material": 0.1,
        "p_structure": 0.95,
        "p_float": 0.9,
        "p_origin": 1.0,
        "p_historical_value": 0.85,
        "p_monument_role": 1.0,
    }
    continuity = service.similarity(
        SimilarityRequest(
            policy_id="preservation-v1",
            left_record_id="ship-state-t1",
            right_record_id="ship-state-t2",
            left_values=left,
            right_values=right,
            threshold=0.85,
        )
    )

    payload = {
        "navigation_system": navigation.model_dump(mode="json"),
        "heritage_system": preservation.model_dump(mode="json"),
        "binary_similarity_example": continuity.model_dump(mode="json"),
    }
    output_path = ROOT / "output" / "demo_results.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    print(f"\nSaved to: {output_path}")


if __name__ == "__main__":
    main()
