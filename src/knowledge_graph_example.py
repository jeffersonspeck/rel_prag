"""Example 3: knowledge graph highlighting by contextual relevance."""

from common import get_profile, print_json

GRAPH_EDGES = [
    {"source": "theseus:ShipOfTheseus", "predicate": "theseus:hasMaterialComposition", "target": "theseus:OriginalAndReplacedParts", "element_id": "p_material"},
    {"source": "theseus:ShipOfTheseus", "predicate": "theseus:hasStructuralOrganization", "target": "theseus:ShipStructure", "element_id": "p_estrutura"},
    {"source": "theseus:ShipOfTheseus", "predicate": "theseus:hasDisposition", "target": "theseus:FloatingDisposition", "element_id": "p_flutuar"},
    {"source": "theseus:ShipOfTheseus", "predicate": "theseus:hasOrigin", "target": "theseus:TheseusHistoricalOrigin", "element_id": "p_origem"},
    {"source": "theseus:ShipOfTheseus", "predicate": "theseus:hasHistoricalValue", "target": "theseus:HistoricalValue", "element_id": "p_valor_historico"},
    {"source": "theseus:ShipOfTheseus", "predicate": "theseus:hasContextualRole", "target": "theseus:MonumentRole", "element_id": "p_papel_monumento"},
]


def highlight_graph(profile_name: str):
    profile = get_profile(profile_name)
    weights = profile["weights"]

    highlighted_edges = []
    for edge in GRAPH_EDGES:
        relevance = weights[edge["element_id"]]
        highlighted_edges.append(
            {
                **edge,
                "relevance": relevance,
                "visibility": "high" if relevance >= 0.8 else "medium" if relevance >= 0.3 else "low",
            }
        )

    highlighted_edges.sort(key=lambda edge: edge["relevance"], reverse=True)

    return {
        "application": "knowledge_graph_visualization",
        "agent": profile["agent"],
        "context": profile["context"],
        "interpretive_role": profile["interpretive_role"],
        "highlighted_edges": highlighted_edges,
    }


if __name__ == "__main__":
    print_json({"sailor": highlight_graph("sailor"), "historian": highlight_graph("historian")})
