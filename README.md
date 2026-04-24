# Ontologia-base do Navio de Teseu + Simulações Epistêmico-Pragmáticas

Este repositório foi reorganizado para ficar **mais informativo** e seguir o princípio pedido:

- a ontologia em `data/theseus_ontology.ttl` contém **somente a estrutura estável** do Navio de Teseu;
- os perfis interpretativos (ex.: marinheiro/historiador) ficam fora da ontologia, como camada de aplicação;
- **todos os exemplos consomem a ontologia-base** como fonte dos elementos `p_i`.

---

## 1) Ideia formal implementada

### 1.1 Estrutura ontológica estável

A ontologia representa apenas:

\[
S(I_{navio}) = \{p_{material}, p_{estrutura}, p_{flutuar}, p_{origem}, p_{valor\_historico}, p_{papel\_monumento}\}
\]

Com valores ontológicos iniciais:

\[
v(p_i)=1.0 \quad \forall p_i \in S(I_{navio})
\]

### 1.2 Relevância pragmática

A interpretação por perfil é calculada por:

\[
Rel_{prag}(I,A,C) = \sum_i w_i(A,C) \cdot v(p_i)
\]

Onde:
- `I` = instância (Navio de Teseu),
- `A` = agente interpretativo,
- `C` = contexto,
- `w_i(A,C)` = peso pragmático,
- `v(p_i)` = valor ontológico do elemento.

---

## 2) Estrutura do projeto

- `data/theseus_ontology.ttl`: ontologia-base com classes, propriedades e elementos do navio.
- `src/create_theseus_ontology.py`: regenera a ontologia-base em Turtle.
- `src/common.py`: carrega a ontologia, valida perfis contra os elementos ontológicos e disponibiliza utilitários comuns.
- `src/demo_relevance.py`: demonstra a fórmula `Rel_prag` com simulação de perfis.
- `src/semantic_query_example.py`: Exemplo 1 (consulta semântica).
- `src/recommendation_example.py`: Exemplo 2 (recomendação).
- `src/knowledge_graph_example.py`: Exemplo 3 (realce de grafo por relevância).
- `src/decision_support_example.py`: Exemplo 4 (apoio à decisão).
- `src/explanation_example.py`: Exemplo 5 (explicação com evidências).
- `src/maintenance_evolution_example.py`: Exemplo 6 (manutenção/evolução de perfis sem alterar ontologia).
- `src/simulate_examples.py`: executa todos os exemplos em lote.

---

## 3) Como executar

```bash
pip install -r requirements.txt
python src/create_theseus_ontology.py
python src/demo_relevance.py
python src/simulate_examples.py
```

Também é possível rodar cada exemplo separadamente:

```bash
python src/semantic_query_example.py
python src/recommendation_example.py
python src/knowledge_graph_example.py
python src/decision_support_example.py
python src/explanation_example.py
python src/maintenance_evolution_example.py
```

---

## 4) Simulação dos exemplos (resumo)

### 4.1 Demo de relevância

Ao rodar `python src/demo_relevance.py`, você verá os elementos carregados da ontologia e o resultado simulado dos perfis.

Exemplo de saída resumida:

- `sailor`: `Rel_prag = 2.20`
- `historian`: `Rel_prag = 4.30`

### 4.2 Exemplo 1 — Consulta semântica

Arquivo: `src/semantic_query_example.py`

- Entrada: perfil (`sailor` ou `historian`)
- Saída: resumo textual + top 3 elementos mais relevantes
- Fórmula usada: `Rel_prag(I,A,C)` para ranking dos elementos

### 4.3 Exemplo 2 — Recomendação

Arquivo: `src/recommendation_example.py`

- Score por item:

\[
score(item)=\sum_i w_i(A,C)\cdot attr_i(item)
\]

- Retorna itens ordenados por aderência ao perfil.

### 4.4 Exemplo 3 — Grafo de conhecimento

Arquivo: `src/knowledge_graph_example.py`

- Cada aresta é ligada a um elemento `p_i`.
- A visualização recebe nível `high/medium/low` conforme o peso `w_i`.

### 4.5 Exemplo 4 — Apoio à decisão

Arquivo: `src/decision_support_example.py`

- Score por alternativa:

\[
score(alt)=\sum_i w_i(A,C)\cdot impact_i(alt)
\]

- Retorna alternativas ranqueadas para cada perfil.

### 4.6 Exemplo 5 — Explicação

Arquivo: `src/explanation_example.py`

- Produz explicação textual baseada nas maiores contribuições de relevância.
- Inclui evidências estruturadas (`weight`, `relevance`, `normalized_contribution`).

### 4.7 Exemplo 6 — Manutenção e evolução

Arquivo: `src/maintenance_evolution_example.py`

- Demonstra adição de um novo perfil (`public_manager`) sem alterar a ontologia-base.
- Mostra separação entre:
  - **núcleo ontológico estável**;
  - **camada pragmática evolutiva**.

---

## 5) Garantia de que “tudo consome a ontologia”

No fluxo atual:

1. `src/common.py` carrega `data/theseus_ontology.ttl`.
2. Extrai elementos `p_i` e seus `v(p_i)`.
3. Valida se cada perfil possui pesos exatamente para os elementos da ontologia.
4. Todos os exemplos reutilizam `common.py`.

Isso assegura que a ontologia do Navio de Teseu é a base única para todo o restante.
