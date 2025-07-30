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
    Voices
)

__version__ = "0.1.4"
__author__ = "Neel Datta"
__email__ = "neeldatta@berkeley.edu"

__all__ = [
    "LemonSliceClient",
    "GenerationRequest", 
    "GenerationResponse",
    "RetryConfig",
    "LemonMeringueError",
    "APIError", 
    "ValidationError",
    "GenerationStatus",
    "Voices"
]