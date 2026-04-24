"""
explanation_example.py

Exemplo 5: sistema de explicação.
Gera uma justificativa textual e estruturada para a interpretação contextual.

Como executar:
    python explanation_example.py
"""

from common import build_base_response, print_json


def explain(profile_name: str):
    response = build_base_response(profile_name)
    top = response["ranking"][:3]

    explanation_parts = [
        f"{item['element']} recebeu peso {item['weight']} e relevância {item['relevance']}"
        for item in top
    ]

    return {
        "application": "explanation",
        "agent": response["agent"],
        "context": response["context"],
        "interpretive_role": response["interpretive_role"],
        "explanation": (
            f"A entidade foi interpretada como {response['interpretive_role']} porque "
            f"os elementos mais influentes foram: " + "; ".join(explanation_parts) + "."
        ),
        "evidence": top,
    }


if __name__ == "__main__":
    print_json({
        "marinheiro": explain("marinheiro"),
        "historiador": explain("historiador"),
    })
