"""File-backed repository for versioned weighting policies W(A,C)."""

from __future__ import annotations

import json
from pathlib import Path

from .exceptions import PolicyNotFoundError, PolicyValidationError
from .models import OntologyEntity, WeightingPolicy


class PolicyRepository:
    def __init__(self, policies_dir: Path) -> None:
        self.policies_dir = policies_dir
        self._policies: dict[str, WeightingPolicy] | None = None

    def _load(self) -> dict[str, WeightingPolicy]:
        policies: dict[str, WeightingPolicy] = {}
        if not self.policies_dir.exists():
            raise PolicyNotFoundError(f"Policy directory not found: {self.policies_dir}")
        for path in sorted(self.policies_dir.glob("*.json")):
            policy = WeightingPolicy.model_validate_json(path.read_text(encoding="utf-8"))
            if policy.policy_id in policies:
                raise PolicyValidationError(f"Duplicate policy id: {policy.policy_id}")
            policies[policy.policy_id] = policy
        if not policies:
            raise PolicyNotFoundError(f"No policy files found in {self.policies_dir}")
        return policies

    @property
    def policies(self) -> dict[str, WeightingPolicy]:
        if self._policies is None:
            self._policies = self._load()
        return self._policies

    def list(self) -> list[WeightingPolicy]:
        return sorted(self.policies.values(), key=lambda item: item.policy_id)

    def get(self, policy_id: str) -> WeightingPolicy:
        try:
            return self.policies[policy_id]
        except KeyError as exc:
            raise PolicyNotFoundError(f"Unknown policy '{policy_id}'.") from exc

    @staticmethod
    def validate_against_entity(policy: WeightingPolicy, entity: OntologyEntity) -> None:
        descriptor_ids = {descriptor.id for descriptor in entity.descriptors}
        weight_ids = set(policy.weights)
        missing = descriptor_ids - weight_ids
        unknown = weight_ids - descriptor_ids
        if policy.ontology_id != entity.ontology_id:
            raise PolicyValidationError(
                f"Policy ontology '{policy.ontology_id}' does not match requested ontology '{entity.ontology_id}'."
            )
        if missing or unknown:
            raise PolicyValidationError(
                f"Policy '{policy.policy_id}' is inconsistent with the descriptor schema. "
                f"Missing={sorted(missing)} Unknown={sorted(unknown)}"
            )
