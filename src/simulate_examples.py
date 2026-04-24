"""Executa todos os exemplos e imprime uma simulação resumida."""

from common import print_json
from decision_support_example import decision_support
from explanation_example import explain
from knowledge_graph_example import highlight_graph
from maintenance_evolution_example import maintenance_report
from recommendation_example import recommend
from semantic_query_example import semantic_query


def main() -> None:
    payload = {
        "semantic_query": {"sailor": semantic_query("sailor"), "historian": semantic_query("historian")},
        "recommendation": {"sailor": recommend("sailor"), "historian": recommend("historian")},
        "knowledge_graph": {"sailor": highlight_graph("sailor"), "historian": highlight_graph("historian")},
        "decision_support": {"sailor": decision_support("sailor"), "historian": decision_support("historian")},
        "explanation": {"sailor": explain("sailor"), "historian": explain("historian")},
        "maintenance_evolution": maintenance_report(),
    }
    print_json(payload)


if __name__ == "__main__":
    main()
