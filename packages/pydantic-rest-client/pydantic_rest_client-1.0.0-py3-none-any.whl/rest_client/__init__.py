"""Pydantic REST Client - library for working with REST APIs with Pydantic validation"""

from .base_rest_client import RestClient, validate_response
from .aiohttp_rest_client import AioHttpRestClient
from .exceptions import (
    RestClientError,
    NetworkError,
    ValidationError,
    ConfigurationError,
    ResponseError,
    TimeoutError,
)

__version__ = "1.0.0"
__author__ = "Damian Sop"
__email__ = "damian.sop.official@gmail.com"

__all__ = [
    "RestClient",
    "AioHttpRestClient",
    "validate_response",
    "RestClientError",
    "NetworkError",
    "ValidationError",
    "ConfigurationError",
    "ResponseError",
    "TimeoutError",
]
