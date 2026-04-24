"""Example 6: maintenance and evolution for ontology-based profiles."""

from copy import deepcopy

from common import PROFILES, print_json


def add_public_manager_profile():
    evolved_profiles = deepcopy(PROFILES)

    evolved_profiles["public_manager"] = {
        "agent": {"id": "theseus:PublicManager", "label": "Public manager"},
        "context": {"id": "theseus:InstitutionalManagementContext", "label": "Institutional management"},
        "interpretive_role": "Public stewardship, preservation, and governance object",
        "weights": {
            "p_material": 0.6,
            "p_estrutura": 0.7,
            "p_flutuar": 0.2,
            "p_origem": 0.7,
            "p_valor_historico": 0.9,
            "p_papel_monumento": 0.8,
        },
    }

    return evolved_profiles


def maintenance_report():
    evolved_profiles = add_public_manager_profile()

    return {
        "application": "ontology_maintenance_and_evolution",
        "original_profiles": list(PROFILES.keys()),
        "new_profile_added": "public_manager",
        "changed_ontology_structure": False,
        "message": (
            "The ontology structure for the entity remains unchanged. "
            "Evolution occurs by adding a new interpretive profile."
        ),
        "comparison": {
            "sailor": {
                "agent": PROFILES["sailor"]["agent"],
                "context": PROFILES["sailor"]["context"],
                "weights": PROFILES["sailor"]["weights"],
            },
            "historian": {
                "agent": PROFILES["historian"]["agent"],
                "context": PROFILES["historian"]["context"],
                "weights": PROFILES["historian"]["weights"],
            },
            "public_manager": {
                "agent": evolved_profiles["public_manager"]["agent"],
                "context": evolved_profiles["public_manager"]["context"],
                "weights": evolved_profiles["public_manager"]["weights"],
            },
        },
    }


if __name__ == "__main__":
    print_json(maintenance_report())
