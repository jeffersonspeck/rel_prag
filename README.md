# Ship of Theseus Base Ontology + Epistemic-Pragmatic Simulations

This repository was reorganized to be **more informative** and to follow the requested principle:

- the ontology in `data/theseus_ontology.ttl` contains **only the stable structure** of the Ship of Theseus;
- interpretive profiles (e.g., sailor/historian) remain outside the ontology as an application layer;
- **all examples consume the base ontology** as the source of elements `p_i`.

---

## 1) Implemented formal idea

### 1.1 Stable ontological structure

The ontology represents only:

\[
S(I_{ship}) = \{p_{material}, p_{estrutura}, p_{flutuar}, p_{origem}, p_{valor\_historico}, p_{papel\_monumento}\}
\]

With initial ontological values:

\[
v(p_i)=1.0 \quad \forall p_i \in S(I_{ship})
\]

### 1.2 Pragmatic relevance

Interpretation by profile is computed as:

\[
Rel_{prag}(I,A,C) = \sum_i w_i(A,C) \cdot v(p_i)
\]

Where:
- `I` = instance (Ship of Theseus),
- `A` = interpretive agent,
- `C` = context,
- `w_i(A,C)` = pragmatic weight,
- `v(p_i)` = ontological value of the element.

---

## 2) Project structure

- `data/theseus_ontology.ttl`: base ontology with classes, properties, and ship elements.
- `src/create_theseus_ontology.py`: regenerates the base ontology in Turtle.
- `src/common.py`: loads the ontology, validates profiles against ontological elements, and provides shared utilities.
- `src/demo_relevance.py`: demonstrates the `Rel_prag` formula with profile simulation.
- `src/semantic_query_example.py`: Example 1 (semantic query).
- `src/recommendation_example.py`: Example 2 (recommendation).
- `src/knowledge_graph_example.py`: Example 3 (relevance-based graph highlighting).
- `src/decision_support_example.py`: Example 4 (decision support).
- `src/explanation_example.py`: Example 5 (explanation with evidence).
- `src/maintenance_evolution_example.py`: Example 6 (profile maintenance/evolution without changing ontology).
- `src/simulate_examples.py`: runs all examples in batch mode.

---

## 3) How to run

```bash
pip install -r requirements.txt
python src/create_theseus_ontology.py
python src/demo_relevance.py
python src/simulate_examples.py
```

You can also run each example separately:

```bash
python src/semantic_query_example.py
python src/recommendation_example.py
python src/knowledge_graph_example.py
python src/decision_support_example.py
python src/explanation_example.py
python src/maintenance_evolution_example.py
```

To run everything at once and generate result JSON files plus an execution PDF:

```bash
python src/run_all_analyses.py
```

This command creates the `output/` folder with:

- `all_responses.json`: aggregated outputs from all scripts.
- `test_results.json`: result of each executed test/command (`PASS`/`FAIL` + details).
- `explainability.json`: traceability of contributions in the `Rel_prag` formula.
- `execution_report.pdf`: consolidated textual execution report.

In the console, final output is presented in natural language (readable text), without printing raw JSON.

---

## 4) Example simulation (summary)

### 4.1 Relevance demo

When running `python src/demo_relevance.py`, you will see ontology-loaded elements and simulated profile results.

Example summarized output:

- `sailor`: `Rel_prag = 2.20`
- `historian`: `Rel_prag = 4.30`

### 4.2 Example 1 — Semantic query

File: `src/semantic_query_example.py`

- Input: profile (`sailor` or `historian`)
- Output: textual summary + top 3 most relevant elements
- Formula used: `Rel_prag(I,A,C)` for element ranking

### 4.3 Example 2 — Recommendation

File: `src/recommendation_example.py`

- Score per item:

\[
score(item)=\sum_i w_i(A,C)\cdot attr_i(item)
\]

- Returns items ordered by profile adherence.

### 4.4 Example 3 — Knowledge graph

File: `src/knowledge_graph_example.py`

- Each edge is linked to one `p_i` element.
- Visualization receives `high/medium/low` level according to weight `w_i`.

### 4.5 Example 4 — Decision support

File: `src/decision_support_example.py`

- Score per alternative:

\[
score(alt)=\sum_i w_i(A,C)\cdot impact_i(alt)
\]

- Returns ranked alternatives for each profile.

### 4.6 Example 5 — Explanation

File: `src/explanation_example.py`

- Produces textual explanation based on highest relevance contributions.
- Includes structured evidence (`weight`, `relevance`, `normalized_contribution`).

### 4.7 Example 6 — Maintenance and evolution

File: `src/maintenance_evolution_example.py`

- Demonstrates adding a new profile (`public_manager`) without changing the base ontology.
- Shows separation between:
  - **stable ontological core**;
  - **evolving pragmatic layer**.

---

## 5) Guarantee that “everything consumes the ontology”

In the current flow:

1. `src/common.py` loads `data/theseus_ontology.ttl`.
2. Extracts elements `p_i` and their `v(p_i)`.
3. Validates that each profile has weights exactly for ontology elements.
4. All examples reuse `common.py`.

This ensures that the Ship of Theseus ontology is the single base for everything else.
