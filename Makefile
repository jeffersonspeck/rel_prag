.PHONY: install ontology api test demo openapi clean

install:
	python -m pip install -e ".[dev]"

ontology:
	python scripts/create_theseus_ontology.py

api:
	uvicorn epm.api:app --reload

test:
	pytest

demo:
	python scripts/run_local_demo.py

openapi:
	python scripts/export_openapi.py

clean:
	rm -rf .pytest_cache .coverage htmlcov output/*.json output/*.jsonl
