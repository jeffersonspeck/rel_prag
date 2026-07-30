"""Domain exceptions returned by the service and API layers."""


class EPMError(Exception):
    """Base exception for model errors."""


class OntologyNotFoundError(EPMError):
    """Raised when an ontology or entity cannot be loaded."""


class PolicyNotFoundError(EPMError):
    """Raised when a weighting policy does not exist."""


class PolicyValidationError(EPMError):
    """Raised when a policy and an ontology descriptor schema disagree."""


class AggregationError(EPMError):
    """Raised when an aggregation request is invalid."""
