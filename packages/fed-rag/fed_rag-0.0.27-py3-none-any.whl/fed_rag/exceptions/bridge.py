"""Exceptions for Bridges."""

from .core import FedRAGError


class BridgeError(FedRAGError):
    """Base bridge error for all bridge-related exceptions."""

    pass


class MissingSpecifiedConversionMethod(BridgeError):
    """Raised when bridge is missing its specified method."""

    pass


class IncompatibleVersionError(FedRAGError):
    """Raised when a fed-rag component is not compatible with the current version."""
