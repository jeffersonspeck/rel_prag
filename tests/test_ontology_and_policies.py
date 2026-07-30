from pathlib import Path

from epm.ontology import OntologyRepository
from epm.policies import PolicyRepository

ROOT = Path(__file__).resolve().parents[1]


def test_stable_ontology_contains_descriptors_but_no_weights():
    repository = OntologyRepository(ROOT / "data")
    entity = repository.get_entity("theseus", "TheseusShip")
    descriptor_ids = {descriptor.id for descriptor in entity.descriptors}
    assert descriptor_ids == {
        "p_material",
        "p_structure",
        "p_float",
        "p_origin",
        "p_historical_value",
        "p_monument_role",
    }
    ttl = (ROOT / "data" / "theseus_ontology.ttl").read_text(encoding="utf-8")
    assert "navigation-v1" not in ttl
    assert "preservation-v1" not in ttl
    assert "defaultValue" not in ttl
    assert "descriptorKind" not in ttl
    assert "DispositionDescriptor" in ttl
    assert "RoleDescriptor" in ttl
    assert all(descriptor.descriptor_kind != "Descriptor" for descriptor in entity.descriptors)


def test_each_policy_has_provenance_and_matches_ontology():
    ontology = OntologyRepository(ROOT / "data").get_entity("theseus", "TheseusShip")
    policies = PolicyRepository(ROOT / "data" / "policies")
    for policy in policies.list():
        policies.validate_against_entity(policy, ontology)
        assert policy.provenance.source
        assert policy.provenance.method
        assert policy.provenance.evidence
        assert policy.provenance.version
        assert set(policy.evaluation.valuations) == {descriptor.id for descriptor in ontology.descriptors}
        assert set(policy.evaluation.comparators) == {descriptor.id for descriptor in ontology.descriptors}


def test_policies_use_the_exact_weight_vectors_from_the_article():
    policies = PolicyRepository(ROOT / "data" / "policies")
    navigation = policies.get("navigation-v1")
    preservation = policies.get("preservation-v1")

    assert navigation.weights == {
        "p_material": 0.2,
        "p_structure": 0.8,
        "p_float": 1.0,
        "p_origin": 0.1,
        "p_historical_value": 0.1,
        "p_monument_role": 0.0,
    }
    assert preservation.weights == {
        "p_material": 0.9,
        "p_structure": 0.4,
        "p_float": 0.1,
        "p_origin": 1.0,
        "p_historical_value": 1.0,
        "p_monument_role": 0.9,
    }
    assert navigation.agent.id == "agent:sailor"
    assert navigation.context.model_dump() == {
        "goal": "Safe navigation",
        "temporal_scope": "Current operational episode",
        "environment": "Maritime operation",
        "roles": ["sailor", "operator"],
        "norms": ["seaworthiness", "safety"],
    }
    assert preservation.agent.id == "agent:historian"
    assert preservation.context.model_dump() == {
        "goal": "Historical preservation",
        "temporal_scope": "Long-term horizon",
        "environment": "Heritage setting",
        "roles": ["historian", "curator"],
        "norms": ["authenticity", "conservation"],
    }
