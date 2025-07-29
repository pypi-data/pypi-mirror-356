# aif_agent_builder_sdk/__init__.py
"""
AIF Agent Builder SDK
Client library for Agent Builders to interact with an AIF Core Service (Issuing Entity & Registry).
Enables requesting Agent Tokens (ATKs) and managing their lifecycle.
"""

from .client import AIFClient, get_default_aif_client
from .exceptions import ( # ADD THE NEW EXCEPTIONS HERE
    AIFSDKBaseException,
    AIFSDKClientError,
    AIFServiceError,
    AIFTokenValidationError,
    AIFSignatureError,
    AIFTokenExpiredError,
    AIFTokenNotYetValidError,
    AIFClaimError,
    AIFMissingClaimError,
    AIFInvalidAudienceError,
    AIFInvalidIssuerError,
    AIFRevokedTokenError,
    AIFRegistryConnectionError,
    AIFNoMatchingKeyError,
    AIFKeyConstructionError,
    AIFJWKSError,
    AIFTimeoutError
)
from .models import (
    ATKIssuanceRequestData,
    IssuedATK,
    ATKRevocationRequestData,
    RevocationStatusResponse, # This is a model for response FROM REG
    JWK,  # This is a model for JWK structure
    JWKS, # This is a model for JWKS structure
    # MessageResponse, # If used by client for some generic server message
    TokenClaims, # If SDK provides decoded claims
    SUPPORTED_AI_MODELS, # Constants
    STANDARD_PERMISSIONS,
    ALLOWED_TRUST_TAG_KEYS
)
from .token_verifier import TokenVerifier, verify_token_with_revocation_check

__version__ = "0.2.0" # Or your current target

__all__ = [
    # Client
    "AIFClient",
    "get_default_aif_client",
    
    # Exceptions
    "AIFSDKBaseException",
    "AIFSDKClientError",
    "AIFServiceError",
    "AIFTokenValidationError",
    "AIFSignatureError",
    "AIFTokenExpiredError",
    "AIFTokenNotYetValidError",
    "AIFClaimError",
    "AIFMissingClaimError",
    "AIFInvalidAudienceError",
    "AIFInvalidIssuerError", # Make sure this is defined in exceptions.py
    "AIFRevokedTokenError",
    "AIFRegistryConnectionError",
    "AIFNoMatchingKeyError",
    "AIFKeyConstructionError",
    "AIFJWKSError",
    "AIFTimeoutError",
    
    # Models
    "ATKIssuanceRequestData",
    "IssuedATK",
    "ATKRevocationRequestData",
    "RevocationStatusResponse",
    "JWK",
    "JWKS",
    # "MessageResponse",
    "TokenClaims",
    
    # Constants
    "SUPPORTED_AI_MODELS",
    "STANDARD_PERMISSIONS",
    "ALLOWED_TRUST_TAG_KEYS",
    
    # Token verification (if AB SDK offers this)
    "TokenVerifier",
    "verify_token_with_revocation_check",
    
    # Version
    "__version__"
]