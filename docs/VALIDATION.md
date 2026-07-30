# Validação técnica executada

A versão entregue foi verificada com:

```bash
PYTHONPATH=src pytest -q
python -m compileall -q src clients scripts tests
PYTHONPATH=src python scripts/run_local_demo.py
```

Resultado da suíte:

```text
7 passed
```

Também foi iniciado um servidor Uvicorn local e executados os dois consumidores HTTP:

```text
navigation-v1   -> unary_contextual_relevance
preservation-v1 -> unary_contextual_relevance
```

Os dois sistemas usaram a mesma entidade e o mesmo estado descritivo, mas retornaram valores distintos por causa das políticas contextuais diferentes.
