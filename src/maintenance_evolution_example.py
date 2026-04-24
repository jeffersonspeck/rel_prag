"""
maintenance_evolution_example.py

Exemplo 6: manutenção e evolução de sistemas baseados em ontologias.
Mostra como um novo perfil interpretativo pode ser adicionado sem alterar
os perfis originais nem a estrutura ontológica principal da entidade.

Como executar:
    python maintenance_evolution_example.py
"""

from copy import deepcopy
from common import PROFILES, print_json


def add_public_manager_profile():
    evolved_profiles = deepcopy(PROFILES)

    evolved_profiles["gestor_publico"] = {
        "agent": {"id": "theseus:PublicManager", "label": "Gestor público"},
        "context": {"id": "theseus:InstitutionalManagementContext", "label": "Gestão institucional"},
        "interpretive_role": "Objeto de gestão, preservação e responsabilidade pública",
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
        "new_profile_added": "gestor_publico",
        "changed_ontology_structure": False,
        "message": (
            "A estrutura ontológica da entidade não foi alterada. "
            "A evolução ocorreu pela inclusão de um novo perfil interpretativo."
        ),
        "comparison": {
            "marinheiro": {
                "agent": PROFILES["marinheiro"]["agent"],
                "context": PROFILES["marinheiro"]["context"],
                "weights": PROFILES["marinheiro"]["weights"],
            },
            "historiador": {
                "agent": PROFILES["historiador"]["agent"],
                "context": PROFILES["historiador"]["context"],
                "weights": PROFILES["historiador"]["weights"],
            },
            "gestor_publico": {
                "agent": evolved_profiles["gestor_publico"]["agent"],
                "context": evolved_profiles["gestor_publico"]["context"],
                "weights": evolved_profiles["gestor_publico"]["weights"],
            },
        },
    }


if __name__ == "__main__":
    print_json(maintenance_report())
