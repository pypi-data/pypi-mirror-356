# aif_agent_builder_sdk/exceptions.py
from typing import Optional, Any, Dict, List, Union
from datetime import datetime # Needed for some exception contexts

class AIFSDKBaseException(Exception): # Added a common base
    """Base exception for all AIF SDK errors."""
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.context = context or {}
    def __str__(self) -> str:
        base = super().__str__()
        if self.context: return f"{base} (Context: {self.context})"
        return base

class AIFSDKClientError(AIFSDKBaseException):
    """Base exception for errors originating from the SDK client itself (e.g., config errors, bad input)."""
    pass

class AIFServiceError(AIFSDKBaseException):
    """
    Exception for errors returned by the AIF Core Service API.
    Includes HTTP status code and error details from the service.
    """
    def __init__(self, message: str, status_code: Optional[int] = None, detail: Optional[str] = None, context: Optional[Dict[str, Any]] = None):
        super().__init__(message, context)
        self.status_code = status_code
        self.detail = detail

    def __str__(self):
        parts = [f"AIF Service Error: {self.message}"]
        if self.status_code:
            parts.append(f"Status: {self.status_code}")
        if self.detail:
            parts.append(f"Detail: {self.detail}")
        if self.context:
            parts.append(f"Context: {self.context}")
        return " | ".join(parts)


# --- Exceptions for TokenVerifier utility (if used by AB SDK) ---
# These mirror what an SP SDK might have, as verification logic is similar.

class AIFTokenValidationError(AIFSDKClientError): # Inherit from ClientError as it's SDK validating
    """Base class for token validation failures by the SDK's TokenVerifier."""
    def __init__(self, message: str, claim_name: Optional[str] = None, 
                 expected: Any = None, actual: Any = None, context: Optional[Dict[str, Any]] = None):
        super().__init__(message, context)
        self.claim_name = claim_name
        self.expected = expected
        self.actual = actual

class AIFSignatureError(AIFTokenValidationError):
    def __init__(self, message: str = "Token signature is invalid.", **kwargs):
        super().__init__(message, **kwargs)

class AIFTokenExpiredError(AIFTokenValidationError):
    def __init__(self, message: str = "Token has expired.", claim_name: str = "exp", actual: Optional[datetime] = None, **kwargs):
        super().__init__(message, claim_name=claim_name, actual=actual, **kwargs)

class AIFTokenNotYetValidError(AIFTokenValidationError):
    def __init__(self, message: str = "Token is not yet valid.", claim_name: str = "nbf", actual: Optional[datetime] = None, **kwargs):
        super().__init__(message, claim_name=claim_name, actual=actual, **kwargs)

class AIFClaimError(AIFTokenValidationError):
    pass

class AIFMissingClaimError(AIFClaimError):
    def __init__(self, claim_name: str, message: Optional[str] = None, **kwargs):
        super().__init__(message or f"Required claim '{claim_name}' is missing.", claim_name=claim_name, **kwargs)

class AIFInvalidAudienceError(AIFClaimError):
    def __init__(self, expected_audiences: Union[str, List[str]], actual_audience: Any, **kwargs):
        super().__init__("Invalid token audience.", claim_name="aud", expected=expected_audiences, actual=actual_audience, **kwargs)

class AIFInvalidIssuerError(AIFClaimError): # Though AB SDK might not check issuer of token it received
    def __init__(self, expected_issuer: str, actual_issuer: Any, **kwargs):
        super().__init__("Invalid token issuer.", claim_name="iss", expected=expected_issuer, actual=actual_issuer, **kwargs)

class AIFRevokedTokenError(AIFTokenValidationError): # If TokenVerifier checks revocation
    def __init__(self, message: str = "Token has been revoked.", jti: Optional[str] = None, **kwargs):
        super().__init__(message, claim_name="jti", actual=jti, **kwargs)
        self.jti = jti

# Network/JWKS related errors for TokenVerifier
class AIFRegistryConnectionError(AIFSDKClientError): # For SDK's attempt to connect
    def __init__(self, message: str, endpoint: Optional[str] = None, status_code: Optional[int] = None, **kwargs):
        super().__init__(message, **kwargs)
        self.endpoint = endpoint
        self.status_code = status_code

class AIFNoMatchingKeyError(AIFSDKClientError):
    def __init__(self, message: str, requested_kid: Optional[str] = None, available_kids: Optional[List[Optional[str]]] = None, **kwargs):
        super().__init__(message, **kwargs)
        self.requested_kid = requested_kid
        self.available_kids = available_kids or []

class AIFKeyConstructionError(AIFSDKClientError):
    def __init__(self, message: str, kid: Optional[str] = None, key_type: Optional[str] = None, **kwargs):
        super().__init__(message, **kwargs)
        self.kid = kid
        self.key_type = key_type

class AIFJWKSError(AIFSDKClientError):
    def __init__(self, message: str, jwks_url: Optional[str] = None, **kwargs):
        super().__init__(message, **kwargs)
        self.jwks_url = jwks_url

class AIFTimeoutError(AIFRegistryConnectionError): # For SDK's HTTP timeouts
    def __init__(self, message: str, operation: Optional[str] = None, timeout_seconds: Optional[float] = None, **kwargs):
        super().__init__(message, operation=operation, timeout_seconds=timeout_seconds, **kwargs) # Pass to AIFSDKBaseException
        self.operation = operation
        self.timeout_seconds = timeout_seconds