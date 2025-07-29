# Pydantic REST Client

A lightweight, async HTTP client for Python with Pydantic validation support.

## Features

- **Async HTTP client** using aiohttp
- **Pydantic validation** for request/response data
- **Header management** with global and per-request headers
- **Session reuse** for better performance
- **Error handling** with custom exceptions
- **Type hints** throughout the codebase

## Installation

```bash
pip install pydantic-rest-client
```

## Quick Start

```python
import asyncio
from pydantic import BaseModel
from rest_client import AioHttpRestClient, validate_response

# Define your Pydantic models
class User(BaseModel):
    id: int
    name: str
    email: str

class CreateUserRequest(BaseModel):
    name: str
    email: str

# Create API client
class UserAPI:
    def __init__(self):
        self.client = AioHttpRestClient(
            base_url='https://api.example.com',
            headers={'Authorization': 'Bearer your-token'}
        )
    
    @validate_response(User)
    async def get_user(self, user_id: int):
        """Get user by ID with automatic validation"""
        return await self.client.get(f'/users/{user_id}')
    
    @validate_response(User)
    async def create_user(self, name: str, email: str):
        """Create user with automatic validation"""
        data = CreateUserRequest(name=name, email=email)
        return await self.client.post('/users', data=data.dict())

# Usage
async def main():
    api = UserAPI()
    
    # Get user
    user, status = await api.get_user(1)
    print(f"User: {user.name}, Status: {status}")
    
    # Create user
    new_user, status = await api.create_user("John Doe", "john@example.com")
    print(f"Created: {new_user.name}, Status: {status}")
    
    # Clean up
    await api.client.close()

asyncio.run(main())
```

## Advanced Usage

### Custom Headers

```python
# Global headers
client = AioHttpRestClient(
    base_url='https://api.example.com',
    headers={'Authorization': 'Bearer token', 'X-API-Version': '1.0'}
)

# Per-request headers
result, status = await client.get('/users/1', headers={'X-Request-ID': '123'})
```

### Error Handling

```python
from rest_client.exceptions import RestClientError, ValidationError

try:
    user, status = await api.get_user(1)
except ValidationError as e:
    print(f"Validation failed: {e}")
except RestClientError as e:
    print(f"Request failed: {e}")
```

### Without Pydantic Validation

```python
# Skip validation for raw data
result, status = await client.get('/raw-data')
print(f"Raw response: {result}")
```

## Testing

### Running Tests

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=rest_client --cov-report=html

# Run simple tests
python test_simple.py

# Run full test suite
python run_tests.py
```

### Local Test API

For testing HTTP requests without external dependencies, we provide a local FastAPI server:

```bash
# Install FastAPI dependencies
pip install fastapi uvicorn[standard]

# Start the test API server
python test_api.py
```

The server will be available at `http://localhost:8000` with the following endpoints:

- `GET /users/{id}` - Get user by ID
- `POST /users` - Create new user
- `PUT /users/{id}` - Update user
- `PATCH /users/{id}` - Partially update user
- `DELETE /users/{id}` - Delete user
- `GET /headers` - Check request headers
- `POST /echo` - Echo request data
- `GET /not-found` - Always returns 404
- `GET /unauthorized` - Always returns 401
- `GET /server-error` - Always returns 500

### Testing with Local API

```bash
# Method 1: Use the provided script (recommended)
python run_api_tests.py

# Method 2: Set environment variable manually
# On Windows:
set TEST_API=1
python -m pytest tests/ -v

# On Linux/Mac:
export TEST_API=1
python -m pytest tests/ -v

# Method 3: Set environment variable inline
# On Windows:
set TEST_API=1 && python -m pytest tests/ -v

# On Linux/Mac:
TEST_API=1 python -m pytest tests/ -v

# Or run the local API demo
python tests/example_local.py
```

### API Documentation

When the test server is running, you can view the interactive API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development

### Project Structure

```
pydantic_rest_client/
├── rest_client/
│   ├── __init__.py
│   ├── base_rest_client.py
│   ├── aiohttp_rest_client.py
│   └── exceptions.py
├── tests/
│   ├── __init__.py
│   ├── example.py
│   ├── example_local.py
│   └── test_example.py
├── test_api.py
├── test_simple.py
├── run_tests.py
├── requirements-dev.txt
└── README.md
```

### Code Quality

```bash
# Format code
black .

# Lint code
flake8 rest_client tests

# Type checking
mypy rest_client

# Run all checks
python run_tests.py
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
