"""
LemonMeringue: Enhanced Python SDK for LemonSlice API

A fluffy layer of reliability and ease-of-use on top of the LemonSlice API.
"""

from .client import (
    LemonSliceClient,
    GenerationRequest,
    GenerationResponse,
    RetryConfig,
    LemonMeringueError,
    APIError,
    ValidationError,
    GenerationStatus,
    Voices,
    quick_generate
)

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

__all__ = [
    "LemonSliceClient",
    "GenerationRequest", 
    "GenerationResponse",
    "RetryConfig",
    "LemonMeringueError",
    "APIError", 
    "ValidationError",
    "GenerationStatus",
    "Voices",
    "quick_generate"
]