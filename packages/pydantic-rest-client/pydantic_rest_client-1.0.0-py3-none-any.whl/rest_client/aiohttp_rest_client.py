import aiohttp
import json
from typing import Optional, Dict, Any, Union, Tuple
from aiohttp import ClientSession, ClientResponse

from .base_rest_client import RestClient


class AioHttpRestClient(RestClient):
    def __init__(self, base_url: str, headers: dict | None = None, raise_for_status: bool = False):
        super().__init__(base_url, headers, raise_for_status)
        self._session: Optional[ClientSession] = None

    async def _get_session(self) -> ClientSession:
        """Gets or creates an aiohttp session"""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                trust_env=True, 
                raise_for_status=self.raise_for_status
            )
        return self._session

    async def close(self):
        """Closes the aiohttp session"""
        if self._session and not self._session.closed:
            await self._session.close()

    def _merge_headers(self, request_headers: dict | None = None) -> dict:
        """Merges base headers with request headers"""
        merged_headers = self.headers.copy()
        if request_headers:
            merged_headers.update(request_headers)
        return merged_headers

    async def _make_request(
        self, 
        method: str, 
        url: str, 
        data: Optional[Union[Dict, list]] = None, 
        headers: Optional[Dict] = None
    ) -> Tuple[Any, int]:
        """
        Common method for executing HTTP requests
        
        Args:
            method: HTTP method (GET, POST, PUT, PATCH, DELETE)
            url: URL for the request
            data: Data to send
            headers: Additional headers
            
        Returns:
            Tuple[Any, int]: (json_data, status_code)
            
        Raises:
            aiohttp.ClientError: For network errors
            json.JSONDecodeError: For JSON parsing errors
        """
        session = await self._get_session()
        merged_headers = self._merge_headers(headers)
        
        # Prepare data for sending
        json_data = None
        if data is not None:
            json_data = json.dumps(data)
        
        try:
            async with session.request(
                method=method,
                url=self.base_url + url,
                data=json_data,
                headers=merged_headers
            ) as response:
                status = response.status
                
                # Check if there's content to parse
                if response.content_length == 0:
                    return None, status
                
                # Try to parse JSON only for successful requests or if necessary
                try:
                    json_data = await response.json()
                except (json.JSONDecodeError, aiohttp.ContentTypeError):
                    # If JSON parsing fails, return text
                    text_data = await response.text()
                    return text_data, status
                
                return json_data, status
                
        except aiohttp.ClientError as e:
            # Re-raise network errors
            raise e
        except Exception as e:
            # Log unexpected errors
            raise RuntimeError(f"Unexpected error during {method} request: {e}") from e

    async def get(self, url: str, headers: Optional[Dict] = None) -> Tuple[Any, int]:
        """Executes GET request"""
        return await self._make_request('GET', url, headers=headers)

    async def delete(self, url: str, headers: Optional[Dict] = None) -> Tuple[Any, int]:
        """Executes DELETE request"""
        return await self._make_request('DELETE', url, headers=headers)

    async def post(self, url: str, data: Optional[Union[Dict, list]] = None, headers: Optional[Dict] = None) -> Tuple[Any, int]:
        """Executes POST request"""
        return await self._make_request('POST', url, data=data, headers=headers)

    async def put(self, url: str, data: Optional[Union[Dict, list]] = None, headers: Optional[Dict] = None) -> Tuple[Any, int]:
        """Executes PUT request"""
        return await self._make_request('PUT', url, data=data, headers=headers)

    async def patch(self, url: str, data: Optional[Union[Dict, list]] = None, headers: Optional[Dict] = None) -> Tuple[Any, int]:
        """Executes PATCH request"""
        return await self._make_request('PATCH', url, data=data, headers=headers)
