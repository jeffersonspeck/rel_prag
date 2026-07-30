# Migração dos fontes anteriores

Os fontes anteriores mantinham pesos duplicados em `common.py` e `demo_relevance.py`, executavam apenas scripts locais e usavam a soma linear diretamente.

## Correspondência

- `create_theseus_ontology.py` -> `scripts/create_theseus_ontology.py`
- `common.py` -> `ontology.py`, `policies.py`, `models.py` e `service.py`
- `demo_relevance.py` -> `engine.py` e endpoint `/v1/relevance`
- exemplos locais -> dois consumidores HTTP em `clients/`
- `run_all_analyses.py` -> `scripts/run_local_demo.py` + `pytest`

## Correções principais

1. IDs de descritores foram padronizados em inglês.
2. Pesos foram removidos do código-fonte e colocados em políticas JSON versionadas.
3. A proveniência tornou-se obrigatória.
4. O contexto deixou de ser apenas um rótulo.
5. A agregação tornou-se configurável.
6. A similaridade binária ganhou contrato próprio.
7. Resultados possuem advertências explícitas sobre validade e identidade.
8. A API permite consumo por sistemas independentes.
