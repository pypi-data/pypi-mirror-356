import pytest
import pytest_asyncio
import asyncio
import os
from unittest.mock import AsyncMock, patch, MagicMock
from .example import ApiExample
import json

# Helper to skip API tests if no TEST_API env var
skip_api = pytest.mark.skipif(
    os.environ.get("TEST_API") != "1",
    reason="External API tests are skipped unless TEST_API=1 is set"
)

class AsyncContextManagerMock:
    """Proper async context manager mock"""
    def __init__(self, response):
        self.response = response
    
    async def __aenter__(self):
        return self.response
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return None

class TestApiExample:
    """Tests for ApiExample class"""
    
    @pytest_asyncio.fixture
    async def api_example(self):
        """Fixture for creating ApiExample instance"""
        example = ApiExample()
        yield example
        # Clean up after each test
        try:
            await example.client.close()
        except:
            pass

    @skip_api
    @pytest.mark.asyncio
    async def test_get_user_success(self, api_example):
        """Test successful GET request"""
        example_data, status_code = await api_example.get_user(2)
        assert status_code == 200
        assert example_data.data.id == 2

    @skip_api
    @pytest.mark.asyncio
    async def test_get_user_not_found(self, api_example):
        """Test GET request with 404 error"""
        example_data, status_code = await api_example.get_not_found_user(23)
        assert status_code == 404

    @skip_api
    @pytest.mark.asyncio
    async def test_delete_user_success(self, api_example):
        """Test successful DELETE request"""
        example_data, status_code = await api_example.delete_user()
        assert status_code == 204

    @skip_api
    @pytest.mark.asyncio
    async def test_post_user_success(self, api_example):
        """Test successful POST request"""
        example_data, status_code = await api_example.post_user(name='Damian', job='developer')
        assert status_code == 201
        assert example_data.name == 'Damian'

    @skip_api
    @pytest.mark.asyncio
    async def test_put_user_success(self, api_example):
        """Test successful PUT request"""
        example_data, status_code = await api_example.put_user()
        assert status_code == 200
        assert example_data.name == 'Damian'

    @skip_api
    @pytest.mark.asyncio
    async def test_patch_user_success(self, api_example):
        """Test successful PATCH request"""
        example_data, status_code = await api_example.patch_user()
        assert status_code == 200
        assert example_data.name == 'Damian'

    @skip_api
    @pytest.mark.asyncio
    async def test_get_user_with_headers(self, api_example):
        """Test GET request with custom headers"""
        result, status = await api_example.get_user_with_headers(1, {'X-Custom-Header': 'test-value'})
        assert status == 200
        assert result is not None

    @skip_api
    @pytest.mark.asyncio
    async def test_post_user_with_headers(self, api_example):
        """Test POST request with custom headers"""
        result, status = await api_example.post_user_with_headers(
            "John Doe", 
            "Software Engineer", 
            {'Authorization': 'Bearer my-token', 'X-Request-ID': 'test-123'}
        )
        assert status == 201
        assert result is not None


class TestLocalApiExample:
    """Tests for local API example"""
    
    @pytest_asyncio.fixture
    async def local_api_example(self):
        """Fixture for creating local API example"""
        from .example_local import ApiExampleLocal
        example = ApiExampleLocal()
        yield example
        # Clean up after each test
        try:
            await example.client.close()
        except:
            pass

    @skip_api
    @pytest.mark.asyncio
    async def test_local_get_user_success(self, local_api_example):
        """Test successful GET request to local API"""
        example_data, status_code = await local_api_example.get_user(1)
        assert status_code == 200
        assert example_data.data.id == 1
        assert example_data.data.first_name == "George"

    @skip_api
    @pytest.mark.asyncio
    async def test_local_get_user_not_found(self, local_api_example):
        """Test GET request with 404 error to local API"""
        example_data, status_code = await local_api_example.get_not_found_user(999)
        assert status_code == 404

    @skip_api
    @pytest.mark.asyncio
    async def test_local_post_user_success(self, local_api_example):
        """Test successful POST request to local API"""
        example_data, status_code = await local_api_example.post_user("Test User", "Developer")
        assert status_code == 201
        assert example_data.name == "Test User"
        assert example_data.job == "Developer"
        assert example_data.id is not None

    @skip_api
    @pytest.mark.asyncio
    async def test_local_headers(self, local_api_example):
        """Test custom headers with local API"""
        result, status = await local_api_example.test_headers({
            'X-Custom-Header': 'test-value',
            'Authorization': 'Bearer my-token'
        })
        assert status == 200
        assert result is not None

    @skip_api
    @pytest.mark.asyncio
    async def test_local_echo(self, local_api_example):
        """Test echo endpoint with local API"""
        test_data = {'message': 'Hello, API!'}
        result, status = await local_api_example.test_echo(test_data)
        assert status == 200
        assert result is not None


class TestAioHttpRestClient:
    """Tests for AioHttpRestClient class"""
    
    @pytest_asyncio.fixture
    async def client(self):
        """Fixture for creating client"""
        from rest_client import AioHttpRestClient
        client = AioHttpRestClient('https://api.example.com')
        yield client
        # Clean up after each test
        try:
            await client.close()
        except:
            pass

    @pytest.mark.asyncio
    async def test_client_initialization(self):
        """Test client initialization"""
        from rest_client import AioHttpRestClient
        
        # Test with valid parameters
        client = AioHttpRestClient('https://api.example.com')
        assert client.base_url == 'https://api.example.com'
        assert client.headers['Content-Type'] == 'application/json'
        
        # Test with custom headers
        custom_headers = {'Authorization': 'Bearer token'}
        client = AioHttpRestClient('https://api.example.com', headers=custom_headers)
        assert client.headers['Authorization'] == 'Bearer token'
        assert client.headers['Content-Type'] == 'application/json'
        
        # Clean up
        await client.close()

    @pytest.mark.asyncio
    async def test_client_initialization_errors(self):
        """Test client initialization errors"""
        from rest_client import AioHttpRestClient
        
        # Test with empty URL
        with pytest.raises(ValueError, match="base_url cannot be empty"):
            AioHttpRestClient('')
        
        # Test with wrong header type
        with pytest.raises(TypeError, match="headers must be a dictionary"):
            AioHttpRestClient('https://api.example.com', headers=123)  # type: ignore

    @pytest.mark.asyncio
    async def test_merge_headers(self, client):
        """Test header merging"""
        # Test without additional headers
        merged = client._merge_headers()
        assert merged == client.headers
        
        # Test with additional headers
        custom_headers = {'X-Custom': 'value'}
        merged = client._merge_headers(custom_headers)
        assert merged['Content-Type'] == 'application/json'
        assert merged['X-Custom'] == 'value'
        
        # Test overriding existing headers
        override_headers = {'Content-Type': 'text/plain'}
        merged = client._merge_headers(override_headers)
        assert merged['Content-Type'] == 'text/plain'

    @pytest.mark.asyncio
    async def test_session_management(self, client):
        """Test session management"""
        # Test session creation
        session = await client._get_session()
        assert session is not None
        assert not session.closed
        
        # Test session reuse
        session2 = await client._get_session()
        assert session is session2
        
        # Test session closing
        await client.close()
        assert session.closed
        # _session is not None, but should be closed
        assert client._session.closed

    @pytest.mark.asyncio
    async def test_make_request_success(self, client):
        """Test successful request execution"""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.content_length = 100
        mock_response.json.return_value = {'data': 'test'}
        
        mock_session = AsyncMock()
        def request_side_effect(*args, **kwargs):
            return AsyncContextManagerMock(mock_response)
        mock_session.request = request_side_effect
        
        with patch.object(client, '_get_session', return_value=mock_session):
            result, status = await client._make_request('GET', '/test')
            assert status == 200
            assert result == {'data': 'test'}

    @pytest.mark.asyncio
    async def test_make_request_empty_response(self, client):
        """Test request with empty response"""
        mock_response = AsyncMock()
        mock_response.status = 204
        mock_response.content_length = 0
        
        mock_session = AsyncMock()
        def request_side_effect(*args, **kwargs):
            return AsyncContextManagerMock(mock_response)
        mock_session.request = request_side_effect
        
        with patch.object(client, '_get_session', return_value=mock_session):
            result, status = await client._make_request('DELETE', '/test')
            assert status == 204
            assert result is None

    @pytest.mark.asyncio
    async def test_make_request_json_error(self, client):
        """Test request with JSON parsing error"""
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.content_length = 100
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", doc="", pos=0)
        mock_response.text.return_value = "Invalid JSON response"
        
        mock_session = AsyncMock()
        def request_side_effect(*args, **kwargs):
            return AsyncContextManagerMock(mock_response)
        mock_session.request = request_side_effect
        
        with patch.object(client, '_get_session', return_value=mock_session):
            result, status = await client._make_request('GET', '/test')
            assert status == 200
            assert result == "Invalid JSON response"

    @pytest.mark.asyncio
    async def test_make_request_network_error(self, client):
        """Test request with network error"""
        mock_session = AsyncMock()
        mock_session.request.side_effect = Exception("Network error")
        
        with patch.object(client, '_get_session', return_value=mock_session):
            with pytest.raises(RuntimeError, match="Unexpected error during GET request"):
                await client._make_request('GET', '/test')

    @pytest.mark.asyncio
    async def test_http_methods(self, client):
        """Test all HTTP methods"""
        # Mock the _make_request method to avoid actual network calls
        with patch.object(client, '_make_request') as mock_make_request:
            mock_make_request.return_value = ({'test': 'data'}, 200)
            
            # Test GET (no data parameter)
            result, status = await client.get('/test')
            mock_make_request.assert_called_with('GET', '/test', headers=None)
            
            # Test POST
            result, status = await client.post('/test', {'name': 'test'})
            mock_make_request.assert_called_with('POST', '/test', data={'name': 'test'}, headers=None)
            
            # Test PUT
            result, status = await client.put('/test', {'name': 'test'})
            mock_make_request.assert_called_with('PUT', '/test', data={'name': 'test'}, headers=None)
            
            # Test PATCH
            result, status = await client.patch('/test', {'name': 'test'})
            mock_make_request.assert_called_with('PATCH', '/test', data={'name': 'test'}, headers=None)
            
            # Test DELETE (no data parameter)
            result, status = await client.delete('/test')
            mock_make_request.assert_called_with('DELETE', '/test', headers=None)

    @pytest.mark.asyncio
    async def test_close_method(self, client):
        """Test close method"""
        # Create a session first
        session = await client._get_session()
        assert not session.closed
        
        # Close the client
        await client.close()
        assert session.closed
        # _session is not None, but should be closed
        assert client._session.closed


# Demo functions (not tests)
async def demo_api_with_headers():
    """Demo of working with headers"""
    api = ApiExample()
    
    print("=== API Demo with Custom Headers ===")
    
    # GET request with custom headers
    print("\n1. GET request with custom headers:")
    try:
        result, status = await api.get_user_with_headers(1, {'X-Custom-Header': 'test-value'})
        print(f"Status: {status}")
        if result:
            print(f"User: {result.data.first_name}")
    except Exception as e:
        print(f"Error: {e}")
    
    # POST request with custom headers
    print("\n2. POST request with custom headers:")
    try:
        result, status = await api.post_user_with_headers(
            "John Doe", 
            "Software Engineer", 
            {'Authorization': 'Bearer my-token', 'X-Request-ID': 'test-123'}
        )
        print(f"Status: {status}")
        if result:
            print(f"Created user: {result.name} - {result.job}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Clean up
    await api.client.close()


async def demo_api_without_headers():
    """Demo of working without headers"""
    api = ApiExample()
    
    print("\n=== API Demo without Custom Headers ===")
    
    # Regular GET request
    print("\n1. Regular GET request:")
    try:
        result, status = await api.get_user(1)
        print(f"Status: {status}")
        if result:
            print(f"User: {result.data.first_name}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Regular POST request
    print("\n2. Regular POST request:")
    try:
        result, status = await api.post_user("Alice Johnson", "Developer")
        print(f"Status: {status}")
        if result:
            print(f"Created user: {result.name} - {result.job}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Clean up
    await api.client.close()


if __name__ == "__main__":
    # Run demos
    asyncio.run(demo_api_with_headers())
    asyncio.run(demo_api_without_headers())
