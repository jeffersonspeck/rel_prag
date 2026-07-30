# Dois sistemas independentes consumindo a mesma base

## Sistema 1: Navigation Operations System

Arquivo: `clients/navigation_system.py`

- política: `navigation-v1`;
- objetivo: prontidão operacional;
- maior relevância: estrutura e disposição para flutuar;
- usa um requisito conjunto entre `p_structure` e `p_float`;
- consome `POST /v1/relevance`.

## Sistema 2: Heritage Preservation System

Arquivo: `clients/heritage_system.py`

- política: `preservation-v1`;
- objetivo: preservação histórica;
- maior relevância: origem, valor histórico e papel de monumento;
- consome o mesmo endpoint e o mesmo estado da entidade;
- recebe explicação e proveniência próprias da política.

## Por que são sistemas distintos

Os consumidores são processos separados, com objetivos, políticas e responsabilidades diferentes. A integração ocorre somente por HTTP. Eles não importam diretamente classes internas do motor e não modificam o arquivo RDF.

Essa organização demonstra que duas aplicações podem compartilhar a mesma ontologia e ainda manter políticas contextualizadas, auditáveis e versionadas.
