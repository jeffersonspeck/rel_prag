"""Example 5: explanation system with structured evidence."""

from common import build_base_response, print_json


def explain(profile_name: str):
    response = build_base_response(profile_name)
    top = response["ranking"][:3]

    explanation_parts = [f"{item['element']} received weight {item['weight']} and relevance {item['relevance']}" for item in top]

    return {
        "application": "explanation",
        "formula": response["formula"],
        "agent": response["agent"],
        "context": response["context"],
        "interpretive_role": response["interpretive_role"],
        "explanation": (
            f"The entity was interpreted as {response['interpretive_role']} because "
            f"the most influential elements were: {'; '.join(explanation_parts)}."
        ),
        "evidence": top,
    }


if __name__ == "__main__":
    print_json({"sailor": explain("sailor"), "historian": explain("historian")})
