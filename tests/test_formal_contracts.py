import pytest
from pydantic import ValidationError

from epm.aggregators import WeightedInput, weighted_sum
from epm.models import RelevanceRequest, ValuationSpec, WeightingPolicy
from epm.valuations import valuate


def test_context_and_provenance_cannot_be_empty():
    invalid = {
        "policy_id": "invalid",
        "ontology_id": "theseus",
        "agent": {"id": "", "label": "", "kind": "human"},
        "context": {
            "goal": "",
            "temporal_scope": "",
            "environment": "",
            "roles": [],
            "norms": [],
        },
        "interpretive_role": "",
        "weights": {"p_material": 0.1},
        "provenance": {
            "source": "",
            "method": "",
            "evidence": [],
            "timestamp": "2026-01-01T00:00:00Z",
            "version": "",
        },
        "evaluation": {
            "version": "1.0.0",
            "valuations": {"p_material": {"kind": "normalized"}},
            "comparators": {
                "p_material": {"kind": "numeric_closeness", "minimum": 0.0, "maximum": 1.0}
            },
            "relevance_aggregation": {"strategy": "weighted_average", "rules": []},
            "similarity_aggregation": {"strategy": "weighted_average", "rules": []},
            "similarity_threshold": 0.85,
        },
    }

    with pytest.raises(ValidationError):
        WeightingPolicy.model_validate(invalid)


def test_callers_cannot_replace_the_context_bound_aggregator():
    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        RelevanceRequest(
            policy_id="navigation-v1",
            descriptor_values={"p_material": 0.2},
            aggregator="weighted_sum",
        )


def test_domain_valuations_convert_raw_observations_explicitly():
    numeric = ValuationSpec(kind="numeric_range", minimum=0.0, maximum=100.0)
    categorical = ValuationSpec(kind="categorical", categories={"absent": 0.0, "present": 1.0})

    assert valuate(25, numeric) == pytest.approx(0.25)
    assert valuate("present", categorical) == 1.0
    with pytest.raises(ValueError, match="outside the declared range"):
        valuate(120, numeric)


def test_linear_weighted_sum_preserves_the_equation_without_clipping():
    result = weighted_sum(
        [
            WeightedInput(descriptor_id="p_1", value=1.0, weight=0.8),
            WeightedInput(descriptor_id="p_2", value=1.0, weight=0.7),
        ]
    )

    assert result.raw_score == pytest.approx(1.5)
    assert result.score == pytest.approx(1.5)
    assert result.normalized is False
