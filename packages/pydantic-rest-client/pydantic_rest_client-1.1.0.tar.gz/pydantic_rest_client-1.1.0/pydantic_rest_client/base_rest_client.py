from typing import Type, Optional, Any, Union, Dict, List
from pydantic import BaseModel, ValidationError


class RestClient:
    """Base class for REST clients"""
    
    def __init__(self, base_url: str, headers: Optional[Dict[str, str]] = None, raise_for_status: bool = False):
        """
        Initialize REST client
        
        Args:
            base_url: Base URL for API
            headers: Global headers for all requests
            raise_for_status: Raise exceptions for unsuccessful status codes
        """
        if not base_url:
            raise ValueError("base_url cannot be empty")
        
        self.base_url = base_url.rstrip('/')
        self.raise_for_status = raise_for_status
        self.headers = {'Content-Type': 'application/json'}
        
        if headers:
            if not isinstance(headers, dict):
                raise TypeError("headers must be a dictionary")
            self.headers.update(headers)

    @staticmethod
    def get_response_model(base_model: Optional[Type[BaseModel]] = None):
        """
        Decorator for response validation using Pydantic models
        
        Args:
            base_model: Pydantic model for response validation
            
        Returns:
            Decorated function
        """
        def decorator(func):
            async def wrapper(*args, **kwargs):
                try:
                    json_data, status = await func(*args, **kwargs)
                    is_received = status in (200, 201)

                    # If no model is specified, return data as is
                    if base_model is None:
                        return json_data, status
                    
                    # Check that model is a subclass of BaseModel
                    if not issubclass(base_model, BaseModel):
                        raise TypeError(f"{base_model} is not a valid Pydantic model")
                    
                    # If request is unsuccessful, return data as is
                    if not is_received:
                        return json_data, status
                    
                    # Validate data using Pydantic
                    try:
                        if isinstance(json_data, list):
                            return [base_model(**item) for item in json_data], status
                        else:
                            return base_model(**json_data), status
                    except ValidationError as e:
                        # If validation fails, return original data
                        return json_data, status
                        
                except Exception as e:
                    # Re-raise exceptions but add context
                    raise RuntimeError(f"Error in decorated function {func.__name__}: {e}") from e

            return wrapper
        return decorator


# Create a standalone function for easier import
def validate_response(base_model: Optional[Type[BaseModel]] = None):
    """
    Decorator for response validation using Pydantic models
    
    Args:
        base_model: Pydantic model for response validation
        
    Returns:
        Decorated function
    """
    return RestClient.get_response_model(base_model)
