import json

import pytest

from epm.models import RelevanceRequest

STATE = {
    "p_material": 0.2,
    "p_structure": 1.0,
    "p_float": 1.0,
    "p_origin": 1.0,
    "p_historical_value": 0.8,
    "p_monument_role": 1.0,
}


def test_two_systems_consume_same_entity_with_distinct_policies(service):
    navigation = service.relevance(RelevanceRequest(policy_id="navigation-v1", descriptor_values=STATE))
    preservation = service.relevance(RelevanceRequest(policy_id="preservation-v1", descriptor_values=STATE))

    assert navigation.entity_id == preservation.entity_id == "TheseusShip"
    assert navigation.policy_id != preservation.policy_id
    assert navigation.context.goal != preservation.context.goal
    assert navigation.score != preservation.score
    assert navigation.measure_type == "unary_contextual_relevance"
    assert navigation.score == pytest.approx(0.918182, abs=1e-6)
    assert preservation.score == pytest.approx(0.786047, abs=1e-6)
    assert navigation.score_is_normalized is True
    assert preservation.score_is_normalized is True
    assert [row.descriptor_id for row in navigation.contributions] == list(STATE)
    assert [row.descriptor_id for row in preservation.contributions] == list(STATE)


def test_rule_aware_aggregator_can_apply_requirement(service):
    state = {**STATE, "p_float": 0.2}
    request = RelevanceRequest(policy_id="navigation-v1", descriptor_values=state)
    response = service.relevance(request)
    assert response.score == 0.0
    assert "navigation-capability-requirement:requirement-not-met" in response.applied_rules


def test_relevance_requires_an_explicit_complete_observation(service):
    incomplete = {key: value for key, value in STATE.items() if key != "p_monument_role"}
    with pytest.raises(ValueError, match="complete ontology-grounded descriptor schema"):
        service.relevance(RelevanceRequest(policy_id="navigation-v1", descriptor_values=incomplete))


def test_audit_record_preserves_request_policy_and_response(service):
    service.relevance(RelevanceRequest(policy_id="preservation-v1", descriptor_values=STATE))
    event = json.loads(service.audit_logger.path.read_text(encoding="utf-8").splitlines()[-1])

    assert event["payload"]["request"]["descriptor_values"] == STATE
    assert event["payload"]["policy"]["evaluation"]["relevance_aggregation"]["strategy"] == "weighted_average"
    assert event["payload"]["policy"]["provenance"]["version"] == "1.0.0"
    assert event["payload"]["response"]["score"] == pytest.approx(0.786047, abs=1e-6)
