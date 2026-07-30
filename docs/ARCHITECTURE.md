# Arquitetura e decisões de projeto

## 1. Separação de camadas

A implementação possui quatro camadas:

1. **Ontologia estável**: arquivo `data/theseus_ontology.ttl`, contendo a entidade e os descritores admissíveis.
2. **Políticas epistêmico-pragmáticas**: arquivos JSON versionados em `data/policies/`.
3. **Motor computacional**: pacote `src/epm`, responsável por validação, agregação, comparação e explicação.
4. **Integração**: API FastAPI e consumidores externos em `clients/`.

Pesos, agentes, contextos e decisões não são gravados como propriedades intrínsecas do navio. Eles permanecem na política externa e são associados a registros de proveniência.

## 2. Ontologia e OWL

O RDF/OWL é usado para:

- identificar a entidade;
- declarar o esquema estável de descritores;
- tipar e documentar os descritores;
- validar quais propriedades uma política pode ponderar.

O motor Python é usado para:

- calcular relevância e similaridade;
- aplicar agregadores e regras;
- executar limiares;
- produzir explicações e auditoria.

Essa divisão responde à limitação prática de executar cálculos numéricos e políticas contextuais exclusivamente no ecossistema OWL + reasoner.

## 3. Agregação

`Agg_C` é implementado como estratégia substituível:

- `weighted_average`: resultado normalizado e comparável;
- `weighted_sum`: correspondência direta com a equação ilustrativa;
- `rule_aware`: permite sinergia, redundância, requisito e veto.

A soma ponderada não é tratada como definição universal do modelo.

## 4. Relevância e similaridade

### Relevância unária

```text
Rel_prag(I,A,C)
```

Avalia uma entidade sob uma política. É usada pelos sistemas de navegação e preservação.

### Similaridade binária

```text
Sim_prag(I',I'',A,C)
```

Compara dois registros ou estados. O resultado pode apoiar uma decisão de continuidade operacional.

A resposta da API fixa `numerical_identity_claimed=false` e inclui um alerta explícito de não transitividade.
