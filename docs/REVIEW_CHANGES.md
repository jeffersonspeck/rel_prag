# Correspondência entre observações e código

## W(A,C) subespecificado

**Mudança:** `WeightingPolicy` contém agente, contexto, pesos, notas e `ProvenanceRecord`. As políticas são arquivos externos, versionados e auditáveis.

**Não resolvido:** o projeto não define um método universal de elicitação. O método permanece dependente do domínio.

## Natureza do contexto C

**Mudança:** `Context` representa objetivo, escopo temporal, ambiente, papéis e normas, correspondendo a `C=<g,t,e,r,n>`.

**Limite:** não é uma ontologia completa de contexto.

## Pesos como propriedades psicológicas

**Mudança:** os pesos são tratados como política explícita associada a agente e contexto, não como propriedade intrínseca da entidade ou do agente.

## Soma linear e dependências

**Mudança:** foi introduzida uma interface de agregação com média ponderada, soma ponderada e estratégia baseada em regras. Requisitos e vetos demonstram combinações não independentes.

## Função unária versus relação binária

**Mudança:** endpoints, contratos e respostas separados:

- `/v1/relevance` para `Rel_prag(I,A,C)`;
- `/v1/similarity` para `Sim_prag(I',I'',A,C)`.

## Identidade, continuidade e transitividade

**Mudança:** o endpoint binário retorna `operational_continuity_supported`, nunca `IdentityPreserved`. A resposta declara que não há afirmação de identidade numérica e alerta sobre não transitividade.

## Implementação OWL

**Mudança:** RDF/OWL armazena a estrutura estável. Python executa cálculo e política. A divisão está documentada e testada.

## Instanciações e valor prático

**Mudança:** dois sistemas externos realmente consomem a mesma API, com rastreabilidade das contribuições e políticas. Isso demonstra integração e explicabilidade operacional, sem alegar ganho de acurácia.

## Validação

**Atendido parcialmente:** há testes unitários e de integração de software.

**Não atendido:** não há avaliação empírica de utilidade, desempenho ou qualidade dos pesos. Essa validação depende de estudo com domínio e usuários.

## Governança e negociação

**Atendido parcialmente:** políticas são versionadas, comparáveis e auditáveis.

**Não atendido:** o projeto não reconcilia automaticamente políticas conflitantes; essa decisão permanece institucional ou de governança.
