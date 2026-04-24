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
        "message": "A ontologia-base permanece estável; a evolução ocorre nos perfis de interpretação.",
        "changed_ontology_structure": False,
        "original_profiles": list(PROFILES.keys()),
        "new_profile_added": "public_manager",
        "comparison": {
            "sailor": evolved_profiles["sailor"],
            "historian": evolved_profiles["historian"],
            "public_manager": evolved_profiles["public_manager"],
        },
    }


if __name__ == "__main__":
    print_json(maintenance_report())
