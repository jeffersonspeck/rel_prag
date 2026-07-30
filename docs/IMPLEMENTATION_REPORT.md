# Relatório de implementação

## Objetivo

Transformar os scripts anteriores em uma plataforma reutilizável, com uma ontologia estável, políticas externas versionadas, motor de cálculo, API e dois consumidores independentes.

## Problemas corrigidos nos fontes anteriores

1. **Duplicação de pesos**: os perfis apareciam em mais de um módulo. Agora cada política existe uma única vez em `data/policies/`.
2. **Proveniência apenas textual**: agora `ProvenanceRecord` é obrigatório e retorna em todas as decisões.
3. **Contexto como rótulo**: agora o contexto possui objetivo, tempo, ambiente, papéis e normas.
4. **Soma linear rígida**: agora há agregadores substituíveis e regras de interação.
5. **Mistura entre relevância e similaridade**: contratos, endpoints e respostas separados.
6. **Risco de tratar similaridade como identidade**: o campo de continuidade é operacional e a API nunca afirma identidade numérica.
7. **Execução apenas local**: agora sistemas externos consomem o modelo por HTTP.
8. **Ausência de auditoria**: cada avaliação gera registro JSONL.
9. **Ausência de contrato de integração**: OpenAPI exportado em `docs/openapi.json`.
10. **Baixa testabilidade**: suíte automatizada cobre ontologia, políticas, agregação, similaridade e API.

## Dois consumidores implementados

### Navigation Operations System

- seleciona `navigation-v1`;
- usa o mesmo estado do navio e a mesma ontologia;
- prioriza estrutura e disposição para navegar;
- demonstra requisito conjunto entre descritores.

### Heritage Preservation System

- seleciona `preservation-v1`;
- usa o mesmo estado do navio e a mesma ontologia;
- prioriza origem, valor histórico e papel de monumento;
- recebe explicação e proveniência diferentes.

## Pontos deliberadamente não resolvidos

- obtenção universal dos pesos;
- validação empírica dos vetores;
- negociação automática entre políticas;
- teoria de identidade numérica;
- transitividade global da continuidade;
- execução integral do cálculo em OWL.

Esses itens são documentados como limites, não apresentados como capacidades implementadas.
