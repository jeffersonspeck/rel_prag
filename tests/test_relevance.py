from epm.models import InteractionRule, RelevanceRequest

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


def test_rule_aware_aggregator_can_apply_requirement(service):
    state = {**STATE, "p_float": 0.2}
    request = RelevanceRequest(
        policy_id="navigation-v1",
        descriptor_values=state,
        aggregator="rule_aware",
        interaction_rules=[
            InteractionRule(
                rule_id="navigation-requirement",
                kind="requirement",
                descriptors=["p_structure", "p_float"],
                trigger=0.7,
                coefficient=0.0,
                description="Both descriptors are required.",
            )
        ],
    )
    response = service.relevance(request)
    assert response.score == 0.0
    assert "navigation-requirement:requirement-not-met" in response.applied_rules
