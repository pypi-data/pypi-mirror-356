# tests/conftest.py
import pytest
import pytest_asyncio
import os
import jwt
import base64
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, Any
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from dotenv import load_dotenv

from aif_agent_builder_sdk import AIFClient

# Load test environment variables
env_path = Path(__file__).resolve().parent.parent / ".env.test"
if env_path.is_file():
    load_dotenv(dotenv_path=env_path)
else:
    # Fall back to regular .env
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.is_file():
        load_dotenv(dotenv_path=env_path)

# Test configuration
TEST_CORE_SERVICE_URL = os.getenv("AIF_SDK_CORE_URL_TEST", "http://127.0.0.1:5000")
TEST_API_KEY = os.getenv("AIF_SDK_ISSUER_API_KEY_TEST", "test-ab-api-key-12345")

# Test data constants
TEST_ISSUER = "aif://test-issuer.example.com"
TEST_USER_ID = "test-user-001"
TEST_AUDIENCE = "https://test-sp.example.com/api"
TEST_PERMISSIONS = ["read:articles_all", "summarize:text_content_short"]
TEST_PURPOSE = "Test token for SDK testing"
TEST_MODEL_ID = "gpt-4-turbo"


@pytest.fixture(scope="session")
def test_keys():
    """Generate Ed25519 key pair for testing."""
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    
    # Get raw public key bytes for JWKS
    raw_public_key = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )
    x_coordinate = base64.urlsafe_b64encode(raw_public_key).decode().rstrip('=')
    
    # Get PEM format for signing
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    return {
        "private_key": private_key,
        "public_key": public_key,
        "private_pem": private_pem.decode(),
        "x_coordinate": x_coordinate,
        "kid": "test-key-001"
    }


@pytest.fixture(scope="session")
def test_jwks(test_keys):
    """Generate test JWKS."""
    return {
        "keys": [{
            "kty": "OKP",
            "crv": "Ed25519",
            "kid": test_keys["kid"],
            "x": test_keys["x_coordinate"],
            "alg": "EdDSA",
            "use": "sig"
        }]
    }


@pytest.fixture
def create_test_token(test_keys):
    """Factory fixture to create test tokens."""
    def _create_token(
        claims: Dict[str, Any] = None, 
        exp_minutes: int = 15,
        use_test_keys: bool = True
    ) -> str:
        default_claims = {
            "iss": TEST_ISSUER,
            "sub": f"{TEST_ISSUER}/{TEST_MODEL_ID}/{TEST_USER_ID}/test-instance-id",
            "aud": TEST_AUDIENCE,
            "exp": int((datetime.now(timezone.utc) + timedelta(minutes=exp_minutes)).timestamp()),
            "iat": int(datetime.now(timezone.utc).timestamp()),
            "jti": f"test-jti-{int(datetime.now().timestamp())}",
            "permissions": TEST_PERMISSIONS,
            "purpose": TEST_PURPOSE,
        }
        
        if claims:
            default_claims.update(claims)
        
        headers = {
            "alg": "EdDSA" if use_test_keys else "HS256",
            "kid": test_keys["kid"] if use_test_keys else "mock-key",
            "typ": "JWT"
        }
        
        if use_test_keys:
            return jwt.encode(
                default_claims,
                test_keys["private_pem"],
                algorithm="EdDSA",
                headers=headers
            )
        else:
            # For simple mock responses where signature doesn't matter
            return jwt.encode(
                default_claims,
                "test-secret",
                algorithm="HS256",
                headers=headers
            )
    
    return _create_token


@pytest_asyncio.fixture
async def aif_client():
    """Provide an AIFClient instance for testing."""
    client = AIFClient(
        core_service_url=TEST_CORE_SERVICE_URL,
        issuer_api_key=TEST_API_KEY,
        timeout_seconds=5
    )
    yield client
    await client.close()


@pytest.fixture
def mock_atk_response(create_test_token):
    """Generate a mock ATK issuance response."""
    def _mock_response(jti: str = None, **kwargs):
        token = create_test_token(
            claims={"jti": jti} if jti else {},
            use_test_keys=False,
            **kwargs
        )
        return {"atk": token}
    return _mock_response


@pytest.fixture
def mock_revocation_status():
    """Generate a mock revocation status response."""
    def _mock_status(jti: str, is_revoked: bool = False):
        return {
            "jti": jti,
            "is_revoked": is_revoked,
            "checked_at": datetime.now(timezone.utc).isoformat()
        }
    return _mock_status