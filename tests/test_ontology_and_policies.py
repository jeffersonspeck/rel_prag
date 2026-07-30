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


def test_each_policy_has_provenance_and_matches_ontology():
    ontology = OntologyRepository(ROOT / "data").get_entity("theseus", "TheseusShip")
    policies = PolicyRepository(ROOT / "data" / "policies")
    for policy in policies.list():
        policies.validate_against_entity(policy, ontology)
        assert policy.provenance.source
        assert policy.provenance.method
        assert policy.provenance.version
