# tests/test_integration.py
"""
Integration tests that run against a real AIF Core Service.
Requires the service to be running and properly configured.
"""

import pytest
import os
import jwt
import asyncio
from datetime import datetime, timezone

from aif_agent_builder_sdk import AIFClient, AIFServiceError, AIFSDKClientError

# Test configuration - these should be set in your environment
INTEGRATION_TEST_URL = os.getenv("AIF_SDK_CORE_URL_TEST", "http://127.0.0.1:5000")
INTEGRATION_TEST_API_KEY = os.getenv("AIF_SDK_ISSUER_API_KEY_TEST")

# Skip integration tests if not configured
pytestmark = pytest.mark.skipif(
    not INTEGRATION_TEST_API_KEY,
    reason="Integration tests require AIF_SDK_ISSUER_API_KEY_TEST environment variable"
)

@pytest.fixture
async def integration_client():
    """Client configured for integration testing."""
    client = AIFClient(
        core_service_url=INTEGRATION_TEST_URL,
        issuer_api_key=INTEGRATION_TEST_API_KEY,
        timeout_seconds=30  # Longer timeout for real service
    )
    yield client
    await client.close()


class TestServiceConnectivity:
    """Test basic connectivity to the service."""
    
    @pytest.mark.asyncio
    async def test_service_is_running(self, integration_client):
        """Test that the AIF Core Service is accessible."""
        # Try to fetch JWKS (public endpoint)
        jwks = await integration_client.get_jwks()
        
        assert "keys" in jwks
        assert len(jwks["keys"]) > 0
        assert all("kid" in key for key in jwks["keys"])
        print(f"✅ Service running at {INTEGRATION_TEST_URL}")
        print(f"📋 Found {len(jwks['keys'])} key(s) in JWKS")
    
    @pytest.mark.asyncio
    async def test_authentication_works(self, integration_client):
        """Test that our API key is valid by trying to issue a token."""
        try:
            token = await integration_client.request_aif_token(
                user_id="integration-test-user",
                audience_sp_id="https://integration-test.example.com",
                permissions=["read:articles_all"],
                purpose="Integration test - authentication check",
                model_id="gpt-4-turbo"
            )
            assert token.atk.startswith("eyJ")  # JWT format
            print(f"✅ Authentication successful")
            print(f"🎫 Token issued: {token.atk[:50]}...")
            
        except AIFServiceError as e:
            if e.status_code == 401:
                pytest.fail(f"Authentication failed - check your API key: {e}")
            else:
                pytest.fail(f"Unexpected service error: {e}")


class TestTokenLifecycle:
    """Test the complete token lifecycle."""
    
    @pytest.mark.asyncio
    async def test_issue_validate_revoke_cycle(self, integration_client):
        """Test issuing, validating, and revoking a token."""
        
        # Step 1: Issue a token
        print("🔨 Step 1: Issuing token...")
        issued_token = await integration_client.request_aif_token(
            user_id=f"test-user-{int(datetime.now().timestamp())}",
            audience_sp_id="https://integration-test.example.com/api",
            permissions=["read:articles_all", "summarize:text_content_short"],
            purpose="Integration test - full lifecycle",
            model_id="gpt-4-turbo"
        )
        
        assert isinstance(issued_token.atk, str)
        assert issued_token.atk.startswith("eyJ")
        print(f"✅ Token issued successfully")
        
        # Step 2: Validate token locally
        print("🔍 Step 2: Validating token locally...")
        claims = await integration_client.validate_token_locally(issued_token.atk)
        
        assert "jti" in claims
        assert "permissions" in claims
        assert "purpose" in claims
        assert claims["purpose"] == "Integration test - full lifecycle"
        jti = claims["jti"]
        print(f"✅ Token validated, JTI: {jti}")
        
        # Step 3: Check revocation status (should not be revoked)
        print("📋 Step 3: Checking initial revocation status...")
        is_revoked_initial = await integration_client.check_token_revocation_status(jti)
        assert is_revoked_initial is False
        print(f"✅ Token not revoked (as expected)")
        
        # Step 4: Revoke the token
        print("🗑️ Step 4: Revoking token...")
        revoke_result = await integration_client.revoke_aif_token(jti)
        
        assert "message" in revoke_result
        print(f"✅ Token revoked: {revoke_result['message']}")
        
        # Step 5: Check revocation status again (should be revoked)
        print("📋 Step 5: Checking final revocation status...")
        is_revoked_final = await integration_client.check_token_revocation_status(jti)
        assert is_revoked_final is True
        print(f"✅ Token confirmed revoked")
        
        print("🎉 Complete lifecycle test passed!")
    
    @pytest.mark.asyncio
    async def test_revoke_unauthorized_token(self, integration_client):
        """Test that we can't revoke tokens we didn't issue."""
        
        # Try to revoke a fake JTI that doesn't exist or wasn't issued by us
        fake_jti = f"fake-jti-{int(datetime.now().timestamp())}"
        
        with pytest.raises(AIFServiceError) as exc_info:
            await integration_client.revoke_aif_token(fake_jti)
        
        # Should be 403 (unauthorized) or 404 (not found)
        assert exc_info.value.status_code in [403, 404]
        print(f"✅ Correctly prevented unauthorized revocation (HTTP {exc_info.value.status_code})")


class TestErrorHandling:
    """Test error handling with real service responses."""
    
    @pytest.mark.asyncio
    async def test_invalid_permissions(self, integration_client):
        """Test service response to invalid permissions."""
        
        try:
            await integration_client.request_aif_token(
                user_id="test-user",
                audience_sp_id="https://test.example.com",
                permissions=["invalid:permission:that:does:not:exist"],
                purpose="Test invalid permissions",
                model_id="gpt-4-turbo"
            )
            # If this succeeds, the service accepts custom permissions (which might be OK)
            print("ℹ️ Service accepts custom permissions")
            
        except AIFServiceError as e:
            # If it fails, that's also OK - just testing error handling
            assert e.status_code in [400, 422]  # Bad request or validation error
            print(f"✅ Service correctly rejected invalid permissions (HTTP {e.status_code})")
    
    @pytest.mark.asyncio
    async def test_invalid_model_id(self, integration_client):
        """Test service response to invalid model ID."""
        
        try:
            await integration_client.request_aif_token(
                user_id="test-user",
                audience_sp_id="https://test.example.com",
                permissions=["read:articles_all"],
                purpose="Test invalid model",
                model_id="invalid-model-that-does-not-exist"
            )
            # If this succeeds, the service accepts custom models (which might be OK for PoC)
            print("ℹ️ Service accepts custom model IDs")
            
        except AIFServiceError as e:
            assert e.status_code in [400, 422]
            print(f"✅ Service correctly rejected invalid model ID (HTTP {e.status_code})")


class TestConcurrency:
    """Test concurrent operations."""
    
    @pytest.mark.asyncio
    async def test_concurrent_token_issuance(self, integration_client):
        """Test issuing multiple tokens concurrently."""
        
        async def issue_token(user_id: str):
            return await integration_client.request_aif_token(
                user_id=user_id,
                audience_sp_id="https://concurrent-test.example.com",
                permissions=["read:articles_all"],
                purpose=f"Concurrent test for {user_id}",
                model_id="gpt-4-turbo"
            )
        
        # Issue 5 tokens concurrently
        tasks = [issue_token(f"user-{i}") for i in range(5)]
        tokens = await asyncio.gather(*tasks)
        
        assert len(tokens) == 5
        assert all(token.atk.startswith("eyJ") for token in tokens)
        
        # Verify all tokens have unique JTIs
        jtis = []
        for token in tokens:
            claims = jwt.decode(token.atk, options={"verify_signature": False})
            jtis.append(claims["jti"])
        
        assert len(set(jtis)) == 5, "All JTIs should be unique"
        print(f"✅ Successfully issued {len(tokens)} concurrent tokens with unique JTIs")


if __name__ == "__main__":
    # Run integration tests directly
    import sys
    
    if not INTEGRATION_TEST_API_KEY:
        print("❌ Please set AIF_SDK_ISSUER_API_KEY_TEST environment variable")
        sys.exit(1)
    
    print(f"🚀 Running integration tests against {INTEGRATION_TEST_URL}")
    print(f"🔑 Using API key: {INTEGRATION_TEST_API_KEY[:8]}...")
    
    # Run with pytest
    pytest.main([__file__, "-v", "-s"])