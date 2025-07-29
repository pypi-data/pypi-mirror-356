"""Custom exceptions for TSO-LLM."""


class TSOError(Exception):
    """Base exception for TSO errors."""

    pass


class ConfigurationError(TSOError):
    """Raised when there's a configuration issue."""

    pass


class ExtractionError(TSOError):
    """Raised when template extraction fails."""

    pass


class SchemaValidationError(TSOError):
    """Raised when schema validation fails."""

    pass
