"""FastAPI boundary consumed by independent external systems."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, Response

from .audit import AuditLogger
from .exceptions import EPMError
from .models import RelevanceRequest, RelevanceResponse, SimilarityRequest, SimilarityResponse
from .ontology import OntologyRepository
from .policies import PolicyRepository
from .service import EpistemicPragmaticService
from .settings import get_settings

settings = get_settings()
ontology_repository = OntologyRepository(settings.data_dir)
policy_repository = PolicyRepository(settings.data_dir / "policies")
service = EpistemicPragmaticService(
    ontology_repository=ontology_repository,
    policy_repository=policy_repository,
    audit_logger=AuditLogger(settings.audit_path),
)

app = FastAPI(
    title="Epistemic-Pragmatic Model API",
    version="1.0.0",
    description=(
        "Shared service for ontology-grounded unary contextual relevance and binary contextual similarity. "
        "A similarity threshold can support operational continuity, but never asserts numerical identity."
    ),
)


@app.exception_handler(EPMError)
async def epm_error_handler(_, exc: EPMError) -> JSONResponse:
    return JSONResponse(status_code=422, content={"detail": str(exc), "error_type": exc.__class__.__name__})


@app.get("/", include_in_schema=False)
def root() -> dict[str, object]:
    """Human-readable entry point for browsers and API clients."""
    return {
        "service": app.title,
        "version": app.version,
        "status": "running",
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc",
            "openapi": "/openapi.json",
        },
        "endpoints": {
            "health": "GET /health",
            "policies": "GET /v1/policies",
            "policy": "GET /v1/policies/{policy_id}",
            "entity": "GET /v1/ontologies/{ontology_id}/entities/{entity_id}",
            "relevance": "POST /v1/relevance",
            "similarity": "POST /v1/similarity",
        },
        "note": (
            "Unary relevance and binary similarity are task-dependent outputs over the same "
            "ontological basis. Similarity never asserts numerical identity."
        ),
    }


@app.get("/favicon.ico", include_in_schema=False)
def favicon() -> Response:
    """Avoid a harmless browser-generated 404 for favicon.ico."""
    return Response(status_code=204)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "model": "epistemic-pragmatic", "version": app.version}


@app.get("/v1/policies")
def list_policies() -> list[dict]:
    return [policy.model_dump(mode="json") for policy in policy_repository.list()]


@app.get("/v1/policies/{policy_id}")
def get_policy(policy_id: str) -> dict:
    return policy_repository.get(policy_id).model_dump(mode="json")


@app.get("/v1/ontologies/{ontology_id}/entities/{entity_id}")
def get_entity(ontology_id: str, entity_id: str) -> dict:
    return ontology_repository.get_entity(ontology_id, entity_id).model_dump(mode="json")


@app.post("/v1/relevance", response_model=RelevanceResponse)
def relevance(request: RelevanceRequest) -> RelevanceResponse:
    try:
        return service.relevance(request)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.post("/v1/similarity", response_model=SimilarityResponse)
def similarity(request: SimilarityRequest) -> SimilarityResponse:
    try:
        return service.similarity(request)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


def run() -> None:
    import uvicorn

    uvicorn.run("epm.api:app", host=settings.host, port=settings.port, reload=False)
