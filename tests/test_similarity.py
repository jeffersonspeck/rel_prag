from pathlib import Path

import pytest

from epm.exceptions import PolicyValidationError
from epm.models import AggregationSpec, SimilarityRequest
from epm.ontology import OntologyRepository
from epm.policies import PolicyRepository


def test_binary_similarity_is_not_numerical_identity(service):
    left = {
        "p_material": 0.2,
        "p_structure": 1.0,
        "p_float": 1.0,
        "p_origin": 1.0,
        "p_historical_value": 0.8,
        "p_monument_role": 1.0,
    }
    right = {
        "p_material": 0.1,
        "p_structure": 0.95,
        "p_float": 0.9,
        "p_origin": 1.0,
        "p_historical_value": 0.85,
        "p_monument_role": 1.0,
    }
    response = service.similarity(
        SimilarityRequest(
            policy_id="preservation-v1",
            left_record_id="t1",
                right_record_id="t2",
                left_values=left,
                right_values=right,
            )
        )
    assert response.measure_type == "binary_contextual_similarity"
    assert response.numerical_identity_claimed is False
    assert response.operational_continuity_supported is True
    assert response.score_is_normalized is True
    assert all(row.comparator.kind == "numeric_closeness" for row in response.contributions)
    assert any("not guaranteed to be transitive" in warning for warning in response.warnings)


def test_thresholded_weighted_sum_requires_normalized_weights():
    entity = OntologyRepository(Path("data")).get_entity("theseus", "TheseusShip")
    policies = PolicyRepository(Path("data/policies"))
    unsafe = policies.get("preservation-v1").model_copy(deep=True)
    unsafe.evaluation.similarity_aggregation = AggregationSpec(strategy="weighted_sum")

    with pytest.raises(PolicyValidationError, match="weights sum to one"):
        policies.validate_against_entity(unsafe, entity)
