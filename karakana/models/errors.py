"""Typed model provider errors."""


class ModelProviderError(Exception):
    """Base model provider error."""


class ModelProviderNotConfigured(ModelProviderError):
    """Raised when a live call is requested without provider credentials."""


class ModelProviderRequestError(ModelProviderError):
    """Raised when a model request cannot be sent."""


class ModelProviderResponseError(ModelProviderError):
    """Raised when a model response cannot be parsed."""
