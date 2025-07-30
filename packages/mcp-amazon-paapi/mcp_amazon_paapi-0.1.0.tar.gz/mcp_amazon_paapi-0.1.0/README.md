# Amazon PA-API MCP Service

A Model Context Protocol (MCP) service for Amazon Product Advertising API integration. This project
uses the Python SDK officially provided at [Product Advertising API 5.0](https://webservices.amazon.com/paapi5/documentation/).

## Structure

```
mcp-amazon-paapi/
├── src/
│   └── mcp_amazon_paapi/           # Main package
│       ├── __init__.py             # Package initialization
│       ├── service.py              # Amazon PA-API service class with dependency injection
│       ├── server.py               # FastMCP server implementation
│       └── _vendor/                # Vendored dependencies
│           └── paapi5_python_sdk/  # Amazon PA-API Python SDK
├── test/                           # Test suite
│   ├── __init__.py                 # Test package initialization
│   └── test_service.py             # Tests for service module
├── pyproject.toml                  # Project configuration and dependencies
├── uv.lock                         # Dependency lock file
├── README.md                       # Project documentation
```

## Setup

### Initial Setup
```bash
# Sync dependencies from uv.lock (creates virtual environment automatically)
uv sync

# Alternatively, activate the virtual environment manually
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows
```

## Environment Variables

```bash
export PAAPI_ACCESS_KEY="your-access-key"
export PAAPI_SECRET_KEY="your-secret-key"
export PAAPI_PARTNER_TAG="your-partner-tag"
export PAAPI_HOST="webservices.amazon.de"       # optional defaults to webservices.amazon.de
export PAAPI_REGION="eu-west-1"                 # optional defaults to eu-west-1
export PAAPI_MARKETPLACE="www.amazon.de"        # optional, defaults to www.amazon.de
```

## Testing

Run the simple test suite:

```bash
# Run all tests with uv (recommended)
uv run python -m pytest test/test_service.py -v

# Or if you have activated the virtual environment
pytest test/test_service.py -v
```

The test suite includes:
- Service initialization tests
- Configuration management tests  
- Search functionality tests with mocking
- Error handling tests

## Usage

```python
from service import AmazonPAAPIService

# Create service (uses environment variables)
service = AmazonPAAPIService()

# Search for items
items = service.search_items("echo dot", "Electronics", 5)
```

## Running the MCP Server

```bash
# Run directly with uv (recommended)
uv run python server.py

# Or if you have activated the virtual environment
python server.py
```

## Integration in Claude & Cursor

For configuring host, region and markeplace, consult the [Locale Reference for Product Advertising API](https://webservices.amazon.com/paapi5/documentation/locale-reference.html) documentation.

```json
{
  "mcpServers": {
    "amazon-paapi": {
      "command": "uvx",
      "args": [
        "mcp-amazon-paapi"
      ],
      "env": {
        "PAAPI_ACCESS_KEY": "your-access-key",
        "PAAPI_SECRET_KEY": "your-secret-key",
        "PAAPI_PARTNER_TAG": "your-partner-tag",
        "PAAPI_HOST": "webservices.amazon.de",  // select EU or US servers and region
        "PAAPI_REGION": "eu-west-1",
        "PAAPI_MARKETPLACE": "www.amazon.de" // set your preferred marketplace
      }
    }
  }
}
```