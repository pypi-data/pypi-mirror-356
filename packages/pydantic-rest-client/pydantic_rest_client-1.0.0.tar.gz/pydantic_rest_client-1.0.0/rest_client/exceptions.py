"""Custom exceptions for pydantic_rest_client"""
from typing import Any

class RestClientError(Exception):
    """Base exception for all REST client errors"""
    pass


class NetworkError(RestClientError):
    """Exception for network errors"""
    pass


class ValidationError(RestClientError):
    """Exception for data validation errors"""
    pass


class ConfigurationError(RestClientError):
    """Exception for configuration errors"""
    pass


class ResponseError(RestClientError):
    """Exception for server response errors"""
    
    def __init__(self, message: str, status_code: int, response_data: Any = None):

        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data


class TimeoutError(RestClientError):
    """Exception for timeout errors"""
    pass 