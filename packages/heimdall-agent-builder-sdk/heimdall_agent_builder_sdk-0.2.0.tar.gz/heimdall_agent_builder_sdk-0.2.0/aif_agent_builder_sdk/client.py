# Enhanced client.py with additional methods based on core service analysis

import httpx
import os
import json
import logging
import threading
from pathlib import Path
from typing import List, Dict, Optional, Union
from urllib.parse import urljoin
from datetime import datetime, timezone

from .models import ATKIssuanceRequestData, IssuedATK, ATKRevocationRequestData
from .exceptions import AIFSDKClientError, AIFServiceError

logger = logging.getLogger(__name__)

# --- SDK Configuration ---
DEFAULT_AIF_CORE_SERVICE_BASE_URL = os.getenv("AIF_SDK_CORE_URL", "http://127.0.0.1:5000")
DEFAULT_AIF_ISSUER_API_KEY = os.getenv("AIF_SDK_ISSUER_API_KEY")
AIF_API_KEY_HEADER_NAME = "Authorization"

# API Paths - Updated based on core service
ISSUE_ATK_ENDPOINT_PATH = "/api/v1/ie/issue-atk"
REVOKE_ATK_ENDPOINT_PATH = "/reg/revoke-atk"  # Fixed path
JWKS_ENDPOINT_PATH = "/.well-known/jwks.json"
REVOCATION_STATUS_ENDPOINT_PATH = "/reg/revocation-status"

class AIFClient:
    def __init__(
        self,
        core_service_url: Optional[str] = None,
        issuer_api_key: Optional[str] = None,
        timeout_seconds: int = 10
    ):
        """
        Client for Agent Builders to interact with the AIF Core Service (IE/REG).

        Args:
            core_service_url: Base URL of the AIF Core Service.
                              Defaults to AIF_SDK_CORE_URL env var or http://127.0.0.1:5000.
            issuer_api_key: The API key for this Agent Builder to authenticate with the
                            AIF Core Service's protected IE/management endpoints.
                            Defaults to AIF_SDK_ISSUER_API_KEY env var.
            timeout_seconds: Default timeout for HTTP requests.
        """
        self.base_url = (core_service_url or DEFAULT_AIF_CORE_SERVICE_BASE_URL).rstrip('/')
        self.api_key = issuer_api_key or DEFAULT_AIF_ISSUER_API_KEY
        self.timeout = timeout_seconds

        if not self.base_url:
            raise AIFSDKClientError("AIF Core Service URL (core_service_url or AIF_SDK_CORE_URL) must be provided.")
        if not self.api_key:
            raise AIFSDKClientError("AIF Issuer API Key (issuer_api_key or AIF_SDK_ISSUER_API_KEY) must be provided.")
            
        self._http_client: Optional[httpx.AsyncClient] = None
        self._jwks_cache: Optional[Dict] = None  # Cache for JWKS

    async def _get_http_client(self) -> httpx.AsyncClient:
        """Provides an httpx.AsyncClient instance, creating one if needed."""
        if self._http_client is None or self._http_client.is_closed:
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                # CHANGE THIS:
                # AIF_API_KEY_HEADER_NAME: self.api_key
                # TO THIS:
                "Authorization": f"Bearer {self.api_key}"
            }
            self._http_client = httpx.AsyncClient(
                base_url=self.base_url, 
                headers=headers, 
                timeout=self.timeout
            )
        return self._http_client

    async def close(self):
        """Closes the underlying HTTP client. Call when done if using persistent client."""
        if self._http_client and not self._http_client.is_closed:
            await self._http_client.aclose()
            logger.info("AIFClient HTTP session closed.")

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
        
    async def _make_request(
        self, 
        method: str, 
        endpoint_path: str, 
        json_payload: Optional[Dict] = None,
        params: Optional[Dict] = None,
        include_auth_header: bool = True
    ) -> Dict:
        """
        Helper to make a request to the AIF Core Service.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint_path: API endpoint path
            json_payload: JSON body for POST requests
            params: Query parameters for GET requests
            include_auth_header: Whether to include the API key header
        """
        url = endpoint_path
        
        logger.debug(f"SDK Making {method} request to {self.base_url}{url}")
        if json_payload: 
            logger.debug(f"SDK Payload: {json.dumps(json_payload)}")

        try:
            if include_auth_header:
                # Use the main client with auth headers
                client = await self._get_http_client()
                if method.upper() == "POST":
                    response = await client.post(url, json=json_payload)
                elif method.upper() == "GET":
                    response = await client.get(url, params=params)
                else:
                    raise AIFSDKClientError(f"Unsupported HTTP method: {method}")
            else:
                # For public endpoints, create a temporary client without auth
                temp_headers = {"Content-Type": "application/json", "Accept": "application/json"}
                async with httpx.AsyncClient(
                    base_url=self.base_url, 
                    headers=temp_headers, 
                    timeout=self.timeout
                ) as temp_client:
                    if method.upper() == "POST":
                        response = await temp_client.post(url, json=json_payload)
                    elif method.upper() == "GET":
                        response = await temp_client.get(url, params=params)
                    else:
                        raise AIFSDKClientError(f"Unsupported HTTP method: {method}")

            logger.debug(f"SDK Response Status: {response.status_code}")
            logger.debug(f"SDK Response Text: {response.text[:500]}...")

            response.raise_for_status()
            return response.json()
        
        except httpx.HTTPStatusError as http_err:
            detail = str(http_err)
            response_text = http_err.response.text
            try:
                error_json = http_err.response.json()
                if isinstance(error_json, dict) and "detail" in error_json:
                    detail = error_json["detail"]
            except json.JSONDecodeError:
                detail = response_text
            
            logger.error(f"AIF Service HTTP Error ({http_err.response.status_code}) on {method} {url}: {detail}")
            raise AIFServiceError(
                f"AIF Service responded with error: {detail}",
                status_code=http_err.response.status_code,
                detail=response_text
            ) from http_err
        except httpx.RequestError as req_err:
            logger.error(f"AIF Service Request Error on {method} {url}: {req_err}")
            raise AIFSDKClientError(f"Network or request error connecting to AIF Service: {req_err}") from req_err
        except json.JSONDecodeError as json_err:
            logger.error(f"Error parsing JSON response from {method} {url}: {json_err}")
            raise AIFSDKClientError(f"Invalid JSON response from AIF Service: {json_err}") from json_err

    async def request_aif_token(
        self,
        user_id: str,
        audience_sp_id: str,
        permissions: List[str],
        purpose: str,
        model_id: str,
        override_trust_tags: Optional[Dict[str, str]] = None
    ) -> IssuedATK:
        """
        Requests an Agent Token (ATK) from the AIF Core Service's IE endpoint.
        
        Args:
            user_id: Identifier for the end-user delegating the agent
            audience_sp_id: The intended Service Provider audience for this token
            permissions: List of permission strings (e.g., ["read:articles_all"])
            purpose: Description of the task this token is for
            model_id: Identifier of the AI model used
            override_trust_tags: Optional trust metadata overrides
            
        Returns:
            IssuedATK containing the signed JWT token
            
        Raises:
            AIFServiceError: If the service returns an error
            AIFSDKClientError: If there's a client-side error
        """
        request_data = ATKIssuanceRequestData(
            user_id=user_id,
            audience_sp_id=audience_sp_id,
            permissions=permissions,
            purpose=purpose,
            model_id=model_id,
            override_trust_tags=override_trust_tags
        )
        
        response_dict = await self._make_request(
            "POST", 
            ISSUE_ATK_ENDPOINT_PATH, 
            json_payload=request_data.model_dump()
        )
        return IssuedATK(**response_dict)

    async def revoke_aif_token(self, jti: str) -> Dict:
        """
        Requests revocation of an ATK by its JTI from the AIF Core Service's REG endpoint.
        
        Requires authentication - only the original issuer (Agent Builder) can revoke their tokens.
        
        Args:
            jti: The JWT ID of the token to revoke
            
        Returns:
            Dict containing the server's response message
            
        Raises:
            AIFServiceError: If the service returns an error (e.g., 403 for unauthorized access)
            AIFSDKClientError: If there's a client-side error
        """
        if not jti or not jti.strip():
            raise AIFSDKClientError("JTI cannot be empty")
        
        request_data = ATKRevocationRequestData(jti=jti.strip())
        
        # Authentication required - only the token issuer can revoke their tokens
        response_dict = await self._make_request(
            "POST", 
            REVOKE_ATK_ENDPOINT_PATH, 
            json_payload=request_data.model_dump(),
            include_auth_header=True  # Required for authentication
        )
        return response_dict

    async def get_jwks(self, force_refresh: bool = False) -> Dict:
        """
        Retrieves the JSON Web Key Set (JWKS) from the AIF Core Service.
        
        This is used to verify ATK signatures. The JWKS is cached after first retrieval.
        
        Args:
            force_refresh: If True, bypass cache and fetch fresh JWKS
            
        Returns:
            Dict containing the JWKS with 'keys' array
        """
        if not force_refresh and self._jwks_cache is not None:
            logger.debug("Returning cached JWKS")
            return self._jwks_cache
        
        logger.info("Fetching JWKS from AIF Core Service")
        jwks_dict = await self._make_request(
            "GET", 
            JWKS_ENDPOINT_PATH,
            include_auth_header=False  # JWKS endpoint is public
        )
        
        self._jwks_cache = jwks_dict
        return jwks_dict

    async def check_token_revocation_status(self, jti: str) -> bool:
        """
        Checks if a token has been revoked by querying the REG endpoint.
        
        Args:
            jti: The JWT ID to check
            
        Returns:
            True if the token is revoked, False otherwise
            
        Raises:
            AIFServiceError: If the service returns an error
        """
        response_dict = await self._make_request(
            "GET",
            REVOCATION_STATUS_ENDPOINT_PATH,
            params={"jti": jti},
            include_auth_header=False  # Public endpoint
        )
        
        return response_dict.get("is_revoked", False)

    async def validate_token_locally(self, atk: str) -> Dict:
        """
        Performs basic local validation of an ATK.
        
        This decodes the token without signature verification to extract claims.
        For full validation, the token should be verified against the JWKS.
        
        Args:
            atk: The ATK JWT string
            
        Returns:
            Dict containing the decoded token claims
            
        Raises:
            AIFSDKClientError: If the token is malformed
        """
        try:
            import jwt
            
            # Decode without verification to get claims
            claims = jwt.decode(atk, options={"verify_signature": False})
            
            # Check expiration
            exp = claims.get("exp")
            if exp and datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(timezone.utc):
                raise AIFSDKClientError("Token has expired")
            
            return claims
            
        except jwt.DecodeError as e:
            raise AIFSDKClientError(f"Invalid token format: {e}")
        except Exception as e:
            raise AIFSDKClientError(f"Error validating token: {e}")

    @staticmethod
    def get_aif_authorization_header(atk: Union[str, IssuedATK]) -> Dict[str, str]:
        """
        Creates the HTTP Authorization header for an AIF Token.
        Format: Authorization: AIF-Token <atk_string>
        
        Args:
            atk: Either the ATK string or an IssuedATK object
            
        Returns:
            Dict with Authorization header
        """
        atk_string = atk.atk if isinstance(atk, IssuedATK) else atk
        if not atk_string or not isinstance(atk_string, str):
            raise ValueError("Valid ATK string or IssuedATK object required.")
        return {"Authorization": f"AIF-Token {atk_string}"}

    @staticmethod
    def get_custom_aif_header(atk: Union[str, IssuedATK]) -> Dict[str, str]:
        """
        Creates a custom AIF-Token header.
        Format: AIF-Token: <atk_string>
        
        Args:
            atk: Either the ATK string or an IssuedATK object
            
        Returns:
            Dict with AIF-Token header
        """
        atk_string = atk.atk if isinstance(atk, IssuedATK) else atk
        if not atk_string or not isinstance(atk_string, str):
            raise ValueError("Valid ATK string or IssuedATK object required.")
        return {"AIF-Token": atk_string}

# --- Global convenience functions ---
_default_aif_client_instance: Optional[AIFClient] = None
_client_init_lock = threading.Lock()

def get_default_aif_client() -> AIFClient:
    """
    Gets a default, shared AIFClient instance, initializing if needed.
    Reads configuration from environment variables.
    """
    global _default_aif_client_instance
    if _default_aif_client_instance is None:
        with _client_init_lock:
            if _default_aif_client_instance is None:
                try:
                    from dotenv import load_dotenv
                    env_path = Path(os.getcwd()) / ".env"
                    if env_path.is_file(): 
                        load_dotenv(dotenv_path=env_path)
                except ImportError: 
                    pass  # dotenv not installed

                _default_aif_client_instance = AIFClient()
    return _default_aif_client_instance