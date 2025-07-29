# tests/test_client.py
import pytest
import json
import jwt
from datetime import datetime, timezone
from unittest.mock import patch, AsyncMock, Mock, MagicMock
import httpx

from aif_agent_builder_sdk import (
    AIFClient,
    IssuedATK,
    AIFSDKClientError,
    AIFServiceError,
    get_default_aif_client,
    TokenVerifier,
    verify_token_with_revocation_check
)


class TestClientInitialization:
    """Test AIFClient initialization and configuration."""
    
    def test_client_with_explicit_config(self):
        """Test client initialization with explicit parameters."""
        client = AIFClient(
            core_service_url="https://test.example.com",
            issuer_api_key="test-key-123",
            timeout_seconds=30
        )
        assert client.base_url == "https://test.example.com"
        assert client.api_key == "test-key-123"
        assert client.timeout == 30
    
    def test_client_strips_trailing_slash(self):
        """Test that base URL trailing slash is stripped."""
        client = AIFClient(
            core_service_url="https://test.example.com/",
            issuer_api_key="test-key"
        )
        assert client.base_url == "https://test.example.com"
    
    def test_client_missing_url_error(self):
        """Test error when URL is missing."""
        # Patch both the environment variable and the default constant
        with patch.dict('os.environ', {'AIF_SDK_CORE_URL': ''}, clear=True):
            with patch('aif_agent_builder_sdk.client.DEFAULT_AIF_CORE_SERVICE_BASE_URL', ''):
                with pytest.raises(AIFSDKClientError, match="AIF Core Service URL"):
                    AIFClient(core_service_url=None, issuer_api_key="key")
    
    def test_client_missing_api_key_error(self):
        """Test error when API key is missing."""
        with patch.dict('os.environ', {'AIF_SDK_ISSUER_API_KEY': ''}, clear=True):
            with patch('aif_agent_builder_sdk.client.DEFAULT_AIF_ISSUER_API_KEY', None):
                with pytest.raises(AIFSDKClientError, match="AIF Issuer API Key"):
                    AIFClient(core_service_url="http://test.com", issuer_api_key=None)
    
    @pytest.mark.asyncio
    async def test_context_manager(self):
        """Test client as async context manager."""
        async with AIFClient(
            core_service_url="http://test.com",
            issuer_api_key="test-key"
        ) as client:
            assert isinstance(client, AIFClient)
            assert client._http_client is None  # Not created until first request
        # Client should be closed after exiting context
    
    def test_get_default_client_singleton(self):
        """Test default client singleton behavior."""
        # Clear any existing instance
        import aif_agent_builder_sdk.client
        aif_agent_builder_sdk.client._default_aif_client_instance = None
        
        with patch.dict('os.environ', {
            'AIF_SDK_CORE_URL': 'http://singleton.test.com',
            'AIF_SDK_ISSUER_API_KEY': 'singleton-key'
        }):
            # Also patch the defaults that are read at module import time
            with patch('aif_agent_builder_sdk.client.DEFAULT_AIF_CORE_SERVICE_BASE_URL', 'http://singleton.test.com'):
                with patch('aif_agent_builder_sdk.client.DEFAULT_AIF_ISSUER_API_KEY', 'singleton-key'):
                    client1 = get_default_aif_client()
                    client2 = get_default_aif_client()
                    
                    assert client1 is client2
                    assert client1.base_url == 'http://singleton.test.com'
            
        # Clean up
        aif_agent_builder_sdk.client._default_aif_client_instance = None


class TestTokenIssuance:
    """Test ATK issuance functionality."""
    
    @pytest.mark.asyncio
    async def test_request_token_success(self, aif_client, mock_atk_response):
        """Test successful token issuance."""
        test_jti = "issued-token-123"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_atk_response(jti=test_jti)
        mock_response.raise_for_status.return_value = None
        mock_response.text = json.dumps(mock_atk_response(jti=test_jti))
        
        # Mock the entire client to avoid the temporary client issue
        with patch.object(aif_client, '_get_http_client') as mock_get_client:
            mock_client = AsyncMock()
            mock_client.post.return_value = mock_response
            mock_get_client.return_value = mock_client
            
            result = await aif_client.request_aif_token(
                user_id="test-user",
                audience_sp_id="https://sp.example.com",
                permissions=["read:data"],
                purpose="Test purpose",
                model_id="gpt-4-turbo"
            )
            
            assert isinstance(result, IssuedATK)
            assert result.atk.startswith("eyJ")  # JWT format
    
    @pytest.mark.asyncio
    async def test_request_token_with_trust_tags(self, aif_client, mock_atk_response):
        """Test token issuance with trust tags."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_atk_response()
        mock_response.raise_for_status.return_value = None
        mock_response.text = json.dumps(mock_atk_response())
        
        with patch.object(aif_client, '_get_http_client') as mock_get_client:
            mock_client = AsyncMock()
            mock_client.post.return_value = mock_response
            mock_get_client.return_value = mock_client
            
            result = await aif_client.request_aif_token(
                user_id="test-user",
                audience_sp_id="https://sp.example.com",
                permissions=["read:data"],
                purpose="Test with trust tags",
                model_id="gpt-4-turbo",
                override_trust_tags={
                    "user_verification_level": "email_verified",
                    "agent_environment": "sandbox"
                }
            )
            
            assert isinstance(result, IssuedATK)
            
            # Verify trust tags were sent
            call_args = mock_client.post.call_args
            sent_data = call_args.kwargs['json']
            assert "override_trust_tags" in sent_data
            assert sent_data["override_trust_tags"]["user_verification_level"] == "email_verified"
    
    @pytest.mark.asyncio
    async def test_request_token_service_errors(self, aif_client):
        """Test various service error responses."""
        # 400 Bad Request
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"detail": "Invalid permissions"}
        mock_response.text = '{"detail": "Invalid permissions"}'
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            message="400 Bad Request",
            request=Mock(),
            response=mock_response
        )
        
        with patch.object(aif_client, '_get_http_client') as mock_get_client:
            mock_client = AsyncMock()
            mock_client.post.return_value = mock_response
            mock_get_client.return_value = mock_client
            
            with pytest.raises(AIFServiceError) as exc:
                await aif_client.request_aif_token(
                    user_id="test-user",
                    audience_sp_id="https://sp.example.com",
                    permissions=["read:data"],  # Changed from empty list
                    purpose="Test",
                    model_id="gpt-4-turbo"
                )
            assert exc.value.status_code == 400
            assert "Invalid permissions" in str(exc.value)
    
    @pytest.mark.asyncio
    async def test_request_token_network_error(self, aif_client):
        """Test network error handling."""
        with patch.object(aif_client, '_get_http_client') as mock_get_client:
            mock_client = AsyncMock()
            mock_client.post.side_effect = httpx.ConnectTimeout("Connection timeout")
            mock_get_client.return_value = mock_client
            
            with pytest.raises(AIFSDKClientError, match="Network or request error"):
                await aif_client.request_aif_token(
                    user_id="test-user",
                    audience_sp_id="https://sp.example.com",
                    permissions=["read:data"],
                    purpose="Test",
                    model_id="gpt-4-turbo"
                )


class TestTokenRevocation:
    """Test token revocation functionality."""
    
    @pytest.mark.asyncio
    async def test_revoke_token_success(self, aif_client):
        """Test successful token revocation."""
        test_jti = "revoke-me-123"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": f"JTI '{test_jti}' successfully added to revocation list."}
        mock_response.raise_for_status.return_value = None
        mock_response.text = json.dumps({"message": f"JTI '{test_jti}' successfully added to revocation list."})
        
        with patch.object(aif_client, '_get_http_client') as mock_get_client:
            mock_client = AsyncMock()
            mock_client.post.return_value = mock_response
            mock_get_client.return_value = mock_client
            
            result = await aif_client.revoke_aif_token(test_jti)
            
            assert "message" in result
            assert test_jti in result["message"]
    
    @pytest.mark.asyncio
    async def test_check_revocation_status(self, aif_client, mock_revocation_status):
        """Test checking token revocation status."""
        test_jti = "check-status-123"
        
        # Mock for public endpoint (no auth header)
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_revocation_status(test_jti, is_revoked=False)
        mock_response.raise_for_status.return_value = None
        mock_response.text = json.dumps(mock_revocation_status(test_jti, is_revoked=False))
        
        # We need to mock the AsyncClient constructor for the temporary client
        with patch('httpx.AsyncClient') as mock_async_client_class:
            mock_temp_client = AsyncMock()
            mock_temp_client.get.return_value = mock_response
            mock_temp_client.__aenter__.return_value = mock_temp_client
            mock_temp_client.__aexit__.return_value = None
            mock_async_client_class.return_value = mock_temp_client
            
            is_revoked = await aif_client.check_token_revocation_status(test_jti)
            assert is_revoked is False
            
            # Test revoked status
            mock_response.json.return_value = mock_revocation_status(test_jti, is_revoked=True)
            mock_response.text = json.dumps(mock_revocation_status(test_jti, is_revoked=True))
            
            is_revoked = await aif_client.check_token_revocation_status(test_jti)
            assert is_revoked is True


class TestJWKSOperations:
    """Test JWKS retrieval and caching."""
    
    @pytest.mark.asyncio
    async def test_get_jwks_success(self, aif_client, test_jwks):
        """Test successful JWKS retrieval."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = test_jwks
        mock_response.raise_for_status.return_value = None
        mock_response.text = json.dumps(test_jwks)
        
        # Mock for public endpoint
        with patch('httpx.AsyncClient') as mock_async_client_class:
            mock_temp_client = AsyncMock()
            mock_temp_client.get.return_value = mock_response
            mock_temp_client.__aenter__.return_value = mock_temp_client
            mock_temp_client.__aexit__.return_value = None
            mock_async_client_class.return_value = mock_temp_client
            
            jwks = await aif_client.get_jwks()
            
            assert "keys" in jwks
            assert len(jwks["keys"]) == 1
            assert jwks["keys"][0]["kid"] == "test-key-001"
    
    @pytest.mark.asyncio
    async def test_get_jwks_caching(self, aif_client, test_jwks):
        """Test JWKS caching behavior."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = test_jwks
        mock_response.raise_for_status.return_value = None
        mock_response.text = json.dumps(test_jwks)
        
        with patch('httpx.AsyncClient') as mock_async_client_class:
            mock_temp_client = AsyncMock()
            mock_temp_client.get.return_value = mock_response
            mock_temp_client.__aenter__.return_value = mock_temp_client
            mock_temp_client.__aexit__.return_value = None
            mock_async_client_class.return_value = mock_temp_client
            
            # First call
            jwks1 = await aif_client.get_jwks()
            assert aif_client._jwks_cache is not None
            
            # Second call should use cache (no new request)
            jwks2 = await aif_client.get_jwks()
            assert jwks2 == jwks1
            
            # Verify only one request was made
            assert mock_temp_client.get.call_count == 1
    
    @pytest.mark.asyncio
    async def test_get_jwks_force_refresh(self, aif_client, test_jwks):
        """Test JWKS force refresh."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = test_jwks
        mock_response.raise_for_status.return_value = None
        mock_response.text = json.dumps(test_jwks)
        
        with patch('httpx.AsyncClient') as mock_async_client_class:
            mock_temp_client = AsyncMock()
            mock_temp_client.get.return_value = mock_response
            mock_temp_client.__aenter__.return_value = mock_temp_client
            mock_temp_client.__aexit__.return_value = None
            mock_async_client_class.return_value = mock_temp_client
            
            # Initial request
            jwks1 = await aif_client.get_jwks()
            
            # Force refresh
            jwks2 = await aif_client.get_jwks(force_refresh=True)
            
            # Verify two requests were made
            assert mock_temp_client.get.call_count == 2


class TestTokenValidation:
    """Test token validation functionality."""
    
    @pytest.mark.asyncio
    async def test_validate_token_locally(self, aif_client, create_test_token):
        """Test local token validation."""
        # Valid token
        token = create_test_token(use_test_keys=False)
        claims = await aif_client.validate_token_locally(token)
        
        assert claims["iss"] == "aif://test-issuer.example.com"
        assert "permissions" in claims
        assert "jti" in claims
    
    @pytest.mark.asyncio
    async def test_validate_expired_token(self, aif_client, create_test_token):
        """Test validation of expired token."""
        # Expired token
        token = create_test_token(exp_minutes=-1, use_test_keys=False)
        
        with pytest.raises(AIFSDKClientError, match="expired"):
            await aif_client.validate_token_locally(token)
    
    @pytest.mark.asyncio
    async def test_validate_malformed_token(self, aif_client):
        """Test validation of malformed token."""
        with pytest.raises(AIFSDKClientError, match="Invalid token format"):
            await aif_client.validate_token_locally("not.a.valid.token")
    
    @pytest.mark.asyncio
    async def test_token_verifier(self, test_jwks, create_test_token):
        """Test TokenVerifier functionality."""
        verifier = TokenVerifier(test_jwks)
        
        # Create properly signed token
        token = create_test_token(use_test_keys=True)
        
        # Verify token
        claims = verifier.verify_token(token, audience="https://test-sp.example.com/api")
        
        assert claims["sub"].startswith("aif://")
        assert claims["permissions"] == ["read:articles_all", "summarize:text_content_short"]
        assert claims["purpose"] == "Test token for SDK testing"
    
    @pytest.mark.asyncio
    async def test_verify_token_with_revocation(self, aif_client, test_jwks, create_test_token, mock_revocation_status):
        """Test combined token verification with revocation check."""
        token = create_test_token(use_test_keys=True)
        decoded = jwt.decode(token, options={"verify_signature": False})
        test_jti = decoded["jti"]
        
        # Mock responses
        mock_jwks_response = MagicMock()
        mock_jwks_response.status_code = 200
        mock_jwks_response.json.return_value = test_jwks
        mock_jwks_response.raise_for_status.return_value = None
        mock_jwks_response.text = json.dumps(test_jwks)
        
        mock_revocation_response = MagicMock()
        mock_revocation_response.status_code = 200
        mock_revocation_response.json.return_value = mock_revocation_status(test_jti, is_revoked=False)
        mock_revocation_response.raise_for_status.return_value = None
        mock_revocation_response.text = json.dumps(mock_revocation_status(test_jti, is_revoked=False))
        
        with patch('httpx.AsyncClient') as mock_async_client_class:
            mock_temp_client = AsyncMock()
            
            # Setup different responses based on URL
            async def get_side_effect(url, **kwargs):
                if "jwks.json" in url:
                    return mock_jwks_response
                else:
                    return mock_revocation_response
            
            mock_temp_client.get.side_effect = get_side_effect
            mock_temp_client.__aenter__.return_value = mock_temp_client
            mock_temp_client.__aexit__.return_value = None
            mock_async_client_class.return_value = mock_temp_client
            
            # Should succeed
            claims = await verify_token_with_revocation_check(
                aif_client,
                token,
                audience="https://test-sp.example.com/api"
            )
            assert claims["jti"] == test_jti


class TestUtilityMethods:
    """Test utility methods and edge cases."""
    
    def test_authorization_header_formatting(self):
        """Test authorization header creation."""
        token = "test.jwt.token"
        
        # String token
        header = AIFClient.get_aif_authorization_header(token)
        assert header == {"Authorization": "AIF-Token test.jwt.token"}
        
        # IssuedATK object
        issued = IssuedATK(atk=token)
        header = AIFClient.get_aif_authorization_header(issued)
        assert header == {"Authorization": "AIF-Token test.jwt.token"}
        
        # Custom header
        custom = AIFClient.get_custom_aif_header(token)
        assert custom == {"AIF-Token": token}
        
        # Error cases
        with pytest.raises(ValueError):
            AIFClient.get_aif_authorization_header("")
        
        with pytest.raises(ValueError):
            AIFClient.get_custom_aif_header(None)
    
    @pytest.mark.asyncio
    async def test_invalid_json_response(self, aif_client):
        """Test handling of invalid JSON responses."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = json.JSONDecodeError("Invalid", "doc", 0)
        mock_response.raise_for_status.return_value = None
        mock_response.text = "<html>Not JSON</html>"
        
        with patch.object(aif_client, '_get_http_client') as mock_get_client:
            mock_client = AsyncMock()
            mock_client.post.return_value = mock_response
            mock_get_client.return_value = mock_client
            
            with pytest.raises(AIFSDKClientError, match="Invalid JSON"):
                await aif_client.request_aif_token(
                    user_id="test-user",
                    audience_sp_id="https://sp.example.com",
                    permissions=["read:data"],
                    purpose="Test",
                    model_id="gpt-4-turbo"
                )
class TestRevocationAuthentication:
    """Test revocation endpoint authentication and authorization."""
    
    @pytest.mark.asyncio
    async def test_revoke_token_with_auth_success(self, aif_client):
        """Test successful token revocation with authentication."""
        test_jti = "revoke-with-auth-123"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": f"Token '{test_jti}' successfully revoked"}
        mock_response.raise_for_status.return_value = None
        mock_response.text = json.dumps({"message": f"Token '{test_jti}' successfully revoked"})
        
        with patch.object(aif_client, '_get_http_client') as mock_get_client:
            mock_client = AsyncMock()
            mock_client.post.return_value = mock_response
            mock_get_client.return_value = mock_client
            
            result = await aif_client.revoke_aif_token(test_jti)
            
            # Verify the request was made correctly
            mock_client.post.assert_called_once()
            call_args = mock_client.post.call_args
            
            # Check the endpoint path
            assert call_args[0][0] == "/reg/revoke-atk"
            
            # Check the payload
            payload = call_args.kwargs['json']
            assert payload['jti'] == test_jti
            
            # Verify response
            assert "message" in result
            assert test_jti in result["message"]
    
    @pytest.mark.asyncio
    async def test_revoke_token_unauthorized_403(self, aif_client):
        """Test revocation failure due to unauthorized access (403)."""
        test_jti = "unauthorized-revoke-123"
        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_response.json.return_value = {"detail": "You can only revoke tokens that you have issued"}
        mock_response.text = '{"detail": "You can only revoke tokens that you have issued"}'
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            message="403 Forbidden",
            request=Mock(),
            response=mock_response
        )
        
        with patch.object(aif_client, '_get_http_client') as mock_get_client:
            mock_client = AsyncMock()
            mock_client.post.return_value = mock_response
            mock_get_client.return_value = mock_client
            
            with pytest.raises(AIFServiceError) as exc_info:
                await aif_client.revoke_aif_token(test_jti)
            
            # Verify error details
            error = exc_info.value
            assert error.status_code == 403
            assert "revoke tokens that you have issued" in str(error)
            assert "You can only revoke tokens that you have issued" in error.detail
    
    @pytest.mark.asyncio
    async def test_revoke_token_not_found_404(self, aif_client):
        """Test revocation failure when token is not found (404)."""
        test_jti = "nonexistent-token-123"
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"detail": "Token not found"}
        mock_response.text = '{"detail": "Token not found"}'
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            message="404 Not Found",
            request=Mock(),
            response=mock_response
        )
        
        with patch.object(aif_client, '_get_http_client') as mock_get_client:
            mock_client = AsyncMock()
            mock_client.post.return_value = mock_response
            mock_get_client.return_value = mock_client
            
            with pytest.raises(AIFServiceError) as exc_info:
                await aif_client.revoke_aif_token(test_jti)
            
            # Verify error details
            error = exc_info.value
            assert error.status_code == 404
            assert "Token not found" in str(error)
    
    @pytest.mark.asyncio
    async def test_revoke_token_empty_jti_validation(self, aif_client):
        """Test validation of empty JTI."""
        # Test empty string
        with pytest.raises(AIFSDKClientError, match="JTI cannot be empty"):
            await aif_client.revoke_aif_token("")
        
        # Test whitespace-only string
        with pytest.raises(AIFSDKClientError, match="JTI cannot be empty"):
            await aif_client.revoke_aif_token("   ")
        
        # Test None (though type hints should prevent this)
        with pytest.raises(AIFSDKClientError, match="JTI cannot be empty"):
            await aif_client.revoke_aif_token(None)
    
    @pytest.mark.asyncio
    async def test_revoke_token_strips_whitespace(self, aif_client):
        """Test that JTI whitespace is properly stripped."""
        test_jti = "  whitespace-test-123  "
        expected_jti = "whitespace-test-123"
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": f"Token '{expected_jti}' successfully revoked"}
        mock_response.raise_for_status.return_value = None
        mock_response.text = json.dumps({"message": f"Token '{expected_jti}' successfully revoked"})
        
        with patch.object(aif_client, '_get_http_client') as mock_get_client:
            mock_client = AsyncMock()
            mock_client.post.return_value = mock_response
            mock_get_client.return_value = mock_client
            
            await aif_client.revoke_aif_token(test_jti)
            
            # Verify the JTI was stripped in the request
            call_args = mock_client.post.call_args
            payload = call_args.kwargs['json']
            assert payload['jti'] == expected_jti  # Should be stripped
    
    @pytest.mark.asyncio
    async def test_revoke_token_authentication_header_included(self, aif_client):
        """Test that authentication header is included in revocation requests."""
        test_jti = "auth-header-test-123"
        
        # We need to verify that _make_request is called with include_auth_header=True
        with patch.object(aif_client, '_make_request') as mock_make_request:
            mock_make_request.return_value = {"message": "Success"}
            
            await aif_client.revoke_aif_token(test_jti)
            
            # Verify _make_request was called with correct parameters
            mock_make_request.assert_called_once_with(
                "POST",
                "/reg/revoke-atk",
                json_payload={'jti': test_jti},
                include_auth_header=True
            )


class TestRevocationIntegration:
    """Integration tests for the complete revocation flow."""
    
    @pytest.mark.asyncio
    async def test_issue_and_revoke_token_flow(self, aif_client, mock_atk_response):
        """Test the complete flow of issuing and then revoking a token."""
        # Mock token issuance
        test_jti = "integration-test-123"
        issue_response = mock_atk_response(jti=test_jti)
        
        mock_issue_response = MagicMock()
        mock_issue_response.status_code = 200
        mock_issue_response.json.return_value = issue_response
        mock_issue_response.raise_for_status.return_value = None
        mock_issue_response.text = json.dumps(issue_response)
        
        # Mock token revocation
        revoke_response = {"message": f"Token '{test_jti}' successfully revoked"}
        mock_revoke_response = MagicMock()
        mock_revoke_response.status_code = 200
        mock_revoke_response.json.return_value = revoke_response
        mock_revoke_response.raise_for_status.return_value = None
        mock_revoke_response.text = json.dumps(revoke_response)
        
        with patch.object(aif_client, '_get_http_client') as mock_get_client:
            mock_client = AsyncMock()
            
            # Setup different responses for different endpoints
            def post_side_effect(url, **kwargs):
                if "issue-atk" in url:
                    return mock_issue_response
                elif "revoke-atk" in url:
                    return mock_revoke_response
                else:
                    raise ValueError(f"Unexpected URL: {url}")
            
            mock_client.post.side_effect = post_side_effect
            mock_get_client.return_value = mock_client
            
            # Step 1: Issue token
            issued_token = await aif_client.request_aif_token(
                user_id="test-user",
                audience_sp_id="https://sp.example.com",
                permissions=["read:data"],
                purpose="Integration test",
                model_id="gpt-4-turbo"
            )
            
            # Step 2: Extract JTI from token
            import jwt
            claims = jwt.decode(issued_token.atk, options={"verify_signature": False})
            extracted_jti = claims["jti"]
            
            # Step 3: Revoke token
            revoke_result = await aif_client.revoke_aif_token(extracted_jti)
            
            # Verify the flow worked
            assert "message" in revoke_result
            assert extracted_jti in revoke_result["message"] or "successfully revoked" in revoke_result["message"]
            
            # Verify both endpoints were called
            assert mock_client.post.call_count == 2
    
    @pytest.mark.asyncio
    async def test_revoke_token_with_status_check(self, aif_client, mock_revocation_status):
        """Test revoking a token and then checking its status."""
        test_jti = "status-check-test-123"
        
        # Mock revocation
        revoke_response = {"message": f"Token '{test_jti}' successfully revoked"}
        mock_revoke_response = MagicMock()
        mock_revoke_response.status_code = 200
        mock_revoke_response.json.return_value = revoke_response
        mock_revoke_response.raise_for_status.return_value = None
        mock_revoke_response.text = json.dumps(revoke_response)
        
        # Mock status check (revoked)
        status_response = mock_revocation_status(test_jti, is_revoked=True)
        mock_status_response = MagicMock()
        mock_status_response.status_code = 200
        mock_status_response.json.return_value = status_response
        mock_status_response.raise_for_status.return_value = None
        mock_status_response.text = json.dumps(status_response)
        
        with patch.object(aif_client, '_get_http_client') as mock_get_client:
            with patch('httpx.AsyncClient') as mock_async_client_class:
                # Main client for authenticated requests
                mock_auth_client = AsyncMock()
                mock_auth_client.post.return_value = mock_revoke_response
                mock_get_client.return_value = mock_auth_client
                
                # Temporary client for public status check
                mock_temp_client = AsyncMock()
                mock_temp_client.get.return_value = mock_status_response
                mock_temp_client.__aenter__.return_value = mock_temp_client
                mock_temp_client.__aexit__.return_value = None
                mock_async_client_class.return_value = mock_temp_client
                
                # Step 1: Revoke token
                revoke_result = await aif_client.revoke_aif_token(test_jti)
                assert "message" in revoke_result
                
                # Step 2: Check status
                is_revoked = await aif_client.check_token_revocation_status(test_jti)
                assert is_revoked is True