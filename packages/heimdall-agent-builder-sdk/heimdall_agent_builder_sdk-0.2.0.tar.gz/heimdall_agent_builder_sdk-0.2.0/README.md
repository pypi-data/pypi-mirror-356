# AIF Agent Builder SDK for Python

The official Python SDK for Agent Builders to interact with the Agent Identity Framework (AIF) Core Service.

## Features

- **Token Management**: Issue and revoke Agent Tokens (ATKs)
- **Token Verification**: Verify tokens using JWKS with Ed25519 signatures
- **Revocation Checking**: Check token revocation status
- **Async/Await**: Modern asynchronous Python with httpx
- **Type Hints**: Full type annotations for better IDE support
- **Pydantic Models**: Automatic validation of requests and responses

## Installation

```bash
pip install heimdall-agent-builder-sdk
```

## Quick Install & Import Reference

| Action | Command |
|--------|---------|
| **Install** | `pip install heimdall-agent-builder-sdk` |
| **Import** | `from aif_agent_builder_sdk import AIFClient` |
| **Environment** | `AIF_SDK_CORE_URL`, `AIF_SDK_ISSUER_API_KEY` |

> 💡 **Note**: Package name uses "heimdall" but imports use "aif" to maintain consistency with the Agent Identity Framework (AIF) API.

## Quick Start

### Getting Your API Key

1. **Start your AIF Core Service** (or use a hosted instance)
2. **Visit the web interface** at https://poc.iamheimdall.com
3. **Login with GitHub OAuth** and complete Agent Builder registration
4. **Copy your API key** from the dashboard

### Environment Setup

Create a `.env` file or set environment variables:

```bash
AIF_SDK_CORE_URL=http://localhost:5000
AIF_SDK_ISSUER_API_KEY=your-agent-builder-api-key
```

### Basic Usage

```python
import asyncio
from aif_agent_builder_sdk import AIFClient

async def main():
    # Initialize client
    client = AIFClient()
    
    # Request an Agent Token
    token = await client.request_aif_token(
        user_id="user-123",
        audience_sp_id="https://api.example.com",
        permissions=["read:articles_all", "summarize:text_content_short"],
        purpose="Summarize news articles",
        model_id="gpt-4-turbo"
    )
    
    print(f"Token issued: {token.atk[:50]}...")
    
    # Use the token in API requests to Service Providers
    headers = AIFClient.get_aif_authorization_header(token)
    # headers = {"Authorization": "AIF-Token <token>"}
    
    # Check if token is revoked
    claims = await client.validate_token_locally(token.atk)
    is_revoked = await client.check_token_revocation_status(claims['jti'])
    print(f"Token revoked: {is_revoked}")
    
    # Revoke the token when done
    await client.revoke_aif_token(claims['jti'])
    
    # Clean up
    await client.close()

asyncio.run(main())
```

### Using Context Manager (Recommended)

```python
from aif_agent_builder_sdk import AIFClient

async with AIFClient() as client:
    token = await client.request_aif_token(
        user_id="user-456",
        audience_sp_id="https://api.example.com",
        permissions=["read:user_profile_basic"],
        purpose="Display user profile",
        model_id="gpt-3.5-turbo"
    )
    # Client automatically closes when exiting context
```

### Token Verification

```python
from aif_agent_builder_sdk import verify_token_with_revocation_check

async with AIFClient() as client:
    # Verify token signature and check revocation
    claims = await verify_token_with_revocation_check(
        client,
        token_string,
        audience="https://api.example.com"
    )
    print(f"Token valid! Subject: {claims['sub']}")
```

## Error Handling

```python
from aif_agent_builder_sdk import AIFServiceError, AIFSDKClientError

try:
    token = await client.request_aif_token(...)
except AIFServiceError as e:
    if e.status_code == 401:
        print("Invalid API key - check your credentials")
    elif e.status_code == 403:
        print("Not authorized - check your Agent Builder role")
    else:
        print(f"Service error: {e}")
except AIFSDKClientError as e:
    print(f"Client error: {e}")
```

## Available Models and Permissions

### Supported AI Models

- **GPT Models**: `gpt-4-turbo`, `gpt-3.5-turbo`
- **Claude Models**: `claude-3-opus-20240229`, `claude-3-sonnet-20240229`
- **Gemini**: `gemini-1.5-pro-latest`
- **LLaMA**: `meta-llama/Meta-Llama-3-70B-Instruct`
- **Mistral**: `mistralai/Mistral-7B-Instruct-v0.2`, `mistralai/Mixtral-8x7B-Instruct-v0.1`
- **Others**: `command-r-plus`, `microsoft/phi-2`, etc.

### Standard Permissions

- `read:articles_all` - Read all articles
- `read:articles_topic_tech` - Read tech articles
- `read:user_profile_basic` - Read basic user profile
- `summarize:text_content_short` - Create short summaries
- `summarize:text_content_long` - Create detailed summaries
- `analyze:sentiment_text` - Analyze text sentiment
- `interact:chatbot_basic` - Basic chatbot interactions
- `kms:read_secret_group_A` - Read specific secrets

## Configuration

### Client Options

```python
from aif_agent_builder_sdk import AIFClient

client = AIFClient(
    core_service_url="https://aif.example.com",
    issuer_api_key="your-api-key",
    timeout_seconds=30
)
```

### Environment Variables

- `AIF_SDK_CORE_URL`: Base URL of the AIF Core Service
- `AIF_SDK_ISSUER_API_KEY`: Your Agent Builder API key

## API Reference

### AIFClient Methods

- `request_aif_token()` - Request a new Agent Token
- `revoke_aif_token()` - Revoke a token by JTI (requires ownership)
- `get_jwks()` - Get JSON Web Key Set for signature verification
- `check_token_revocation_status()` - Check if token is revoked
- `validate_token_locally()` - Basic local token validation (no signature check)

### Static Helper Methods

- `get_aif_authorization_header(token)` - Format token for Authorization header
- `get_custom_aif_header(token)` - Format token for custom AIF-Token header

### Models

- `ATKIssuanceRequestData` - Token request payload
- `IssuedATK` - Token response
- `ATKRevocationRequestData` - Revocation request
- `RevocationStatusResponse` - Revocation status
- `JWKS` - JSON Web Key Set

## Common Use Cases

### Issue Token for AI Agent

```python
from aif_agent_builder_sdk import AIFClient

async with AIFClient() as client:
    # Issue token for a content summarization agent
    token = await client.request_aif_token(
        user_id="alice@company.com",
        audience_sp_id="https://news-api.example.com",
        permissions=["read:articles_all", "summarize:text_content_short"],
        purpose="Daily news summary for executive briefing",
        model_id="gpt-4-turbo",
        override_trust_tags={
            "user_verification_level": "email_verified",
            "data_processing_region": "us-east-1"
        }
    )
```

### Batch Token Management

```python
from aif_agent_builder_sdk import AIFClient

async with AIFClient() as client:
    # Issue multiple tokens
    tokens = []
    for user in users:
        token = await client.request_aif_token(
            user_id=user.id,
            audience_sp_id="https://api.service.com",
            permissions=["read:user_profile_basic"],
            purpose=f"Agent for {user.name}",
            model_id="gpt-3.5-turbo"
        )
        tokens.append(token)
    
    # Later, revoke all tokens
    for token in tokens:
        claims = await client.validate_token_locally(token.atk)
        await client.revoke_aif_token(claims['jti'])
```

## Development

### Running Tests

```bash
# Install dev dependencies
pip install -e .[dev]

# Run unit tests
pytest tests/test_client.py -v

# Run integration tests (requires running AIF Core Service)
export AIF_SDK_CORE_URL_TEST=http://127.0.0.1:5000
export AIF_SDK_ISSUER_API_KEY_TEST=your-test-api-key
pytest tests/test_integration.py -v

# Run with coverage
pytest --cov=aif_agent_builder_sdk --cov-report=html
```

### Building and Publishing

```bash
# Build package
python -m build

# Upload to PyPI
twine upload dist/*
```

## Troubleshooting

### Common Issues

**401 Unauthorized**
- Check your API key is correct
- Ensure you're registered as an Agent Builder
- Verify the AIF Core Service URL is correct

**403 Forbidden on Revocation**
- You can only revoke tokens you issued
- Check that the JTI belongs to a token you created

**Connection Errors**
- Ensure the AIF Core Service is running
- Check firewall/network settings
- Verify the service URL format (include http/https)

### Debug Mode

```python
import logging
from aif_agent_builder_sdk import AIFClient

logging.basicConfig(level=logging.DEBUG)

# Now SDK will log detailed request/response info
async with AIFClient() as client:
    token = await client.request_aif_token(...)
```

## License

MIT License - see LICENSE file for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/IAM-Heimdall/heimdall_agent_builder_sdk_python/issues)
- **Repository**: [GitHub Repository](https://github.com/IAM-Heimdall/heimdall_agent_builder_sdk_python)