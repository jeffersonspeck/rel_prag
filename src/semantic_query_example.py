"""Example 1: semantic query organized by interpretive profile."""

from common import build_base_response, print_json


QUERY_TEXT = "Which aspects of the Ship of Theseus are most relevant in this context?"


def semantic_query(profile_name: str):
    response = build_base_response(profile_name)
    top_elements = response["ranking"][:3]

    response.update(
        {
            "application": "semantic_query",
            "query": QUERY_TEXT,
            "answer": {
                "summary": (
                    f"For agent {response['agent']['label']} in context "
                    f"{response['context']['label']}, the entity is interpreted as "
                    f"{response['interpretive_role']}."
                ),
                "most_relevant_elements": top_elements,
                "interpretation_rule": "Higher w_i(A,C) means higher priority over the same ontological base.",
            },
        }
    )

    return response


if __name__ == "__main__":
    print_json({"sailor": semantic_query("sailor"), "historian": semantic_query("historian")})
