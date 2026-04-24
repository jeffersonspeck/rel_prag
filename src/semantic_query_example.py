"""
semantic_query_example.py

Exemplo 1: consulta semântica.
Organiza a resposta conforme o perfil interpretativo selecionado.

Como executar:
    python semantic_query_example.py
"""

from common import build_base_response, print_json


def semantic_query(profile_name: str):
    response = build_base_response(profile_name)
    top_elements = response["ranking"][:3]

    response.update({
        "application": "semantic_query",
        "query": "Quais aspectos do Navio de Teseu são mais relevantes neste contexto?",
        "answer": {
            "summary": (
                f"Para o agente {response['agent']['label']} no contexto "
                f"{response['context']['label']}, a entidade é apresentada como "
                f"{response['interpretive_role']}."
            ),
            "most_relevant_elements": top_elements,
        }
    })

    return response


if __name__ == "__main__":
    print_json({
        "marinheiro": semantic_query("marinheiro"),
        "historiador": semantic_query("historiador"),
    })
