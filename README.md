# Ontologia Epistêmico-Pragmática do Navio de Teseu

Este projeto implementa, em Python, uma representação simples do modelo formulado no texto sobre o Paradoxo do Navio de Teseu e os desafios epistêmicos e pragmáticos da modelagem ontológica.

O projeto contém:

- `data/theseus_ontology.ttl`: ontologia em Turtle com a estrutura estável do navio, agentes, contextos, papéis e vetores de ponderação.
- `src/create_theseus_ontology.py`: script que gera novamente o arquivo TTL.
- `src/demo_relevance.py`: script que carrega os pesos e calcula a função de relevância pragmática.
- `requirements.txt`: dependências Python.

## Como executar

```bash
pip install -r requirements.txt
python src/create_theseus_ontology.py
python src/demo_relevance.py
```

## Ideia formal implementada

A estrutura ontológica estável da instância é representada por:

```text
S(I_navio) = {
  p_material,
  p_estrutura,
  p_flutuar,
  p_origem,
  p_valor_historico,
  p_papel_monumento
}
```

A relevância pragmática é calculada por:

```text
Rel_prag(I,A,C) = soma(w_i(A,C) * v(p_i))
```

No exemplo, os valores `v(p_i)` são inicialmente definidos como 1.0 para todos os elementos ontológicos presentes na instância. Assim, a diferença entre as interpretações decorre dos pesos atribuídos por agente e contexto.
# rel_prag
