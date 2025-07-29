# aif_agent_builder_sdk/token_verifier.py
"""
Token verification utilities for the AIF SDK.
Provides local token verification using JWKS.
"""

import jwt
import base64
import logging
from typing import Dict, Optional, List, Any
from datetime import datetime, timezone
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.backends import default_backend

from .exceptions import AIFSDKClientError

logger = logging.getLogger(__name__)

class TokenVerifier:
    """
    Verifies AIF tokens using JWKS from the core service.
    """
    
    def __init__(self, jwks: Dict[str, Any]):
        """
        Initialize the verifier with a JWKS.
        
        Args:
            jwks: The JSON Web Key Set containing public keys
        """
        self.jwks = jwks
        self._key_cache: Dict[str, ed25519.Ed25519PublicKey] = {}
        self._load_keys()
    
    def _load_keys(self):
        """Load and cache the public keys from JWKS."""
        keys = self.jwks.get("keys", [])
        
        for key_data in keys:
            if key_data.get("kty") != "OKP" or key_data.get("crv") != "Ed25519":
                logger.warning(f"Skipping non-Ed25519 key: {key_data.get('kid')}")
                continue
            
            try:
                # Decode the x coordinate (public key)
                x_bytes = base64.urlsafe_b64decode(key_data["x"] + "==")  # Add padding if needed
                
                # Create Ed25519 public key
                public_key = ed25519.Ed25519PublicKey.from_public_bytes(x_bytes)
                
                # Cache by kid
                kid = key_data.get("kid")
                if kid:
                    self._key_cache[kid] = public_key
                    logger.info(f"Loaded public key with kid: {kid}")
                    
            except Exception as e:
                logger.error(f"Error loading key {key_data.get('kid')}: {e}")
    
    def verify_token(
        self, 
        token: str, 
        audience: Optional[str] = None,
        verify_exp: bool = True,
        verify_aud: bool = True
    ) -> Dict[str, Any]:
        """
        Verify an AIF token signature and claims.
        
        Args:
            token: The JWT token string to verify
            audience: Expected audience claim (if verify_aud is True)
            verify_exp: Whether to verify expiration
            verify_aud: Whether to verify audience
            
        Returns:
            Dict containing the verified token claims
            
        Raises:
            AIFSDKClientError: If verification fails
        """
        try:
            # First decode without verification to get the header
            unverified_header = jwt.get_unverified_header(token)
            kid = unverified_header.get("kid")
            alg = unverified_header.get("alg")
            
            if alg != "EdDSA":
                raise AIFSDKClientError(f"Unsupported algorithm: {alg}")
            
            if not kid:
                raise AIFSDKClientError("Token missing 'kid' header")
            
            # Get the public key for this kid
            public_key = self._key_cache.get(kid)
            if not public_key:
                raise AIFSDKClientError(f"No public key found for kid: {kid}")
            
            # Convert to PEM format for PyJWT
            public_key_pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            
            # Verify the token
            options = {
                "verify_signature": True,
                "verify_exp": verify_exp,
                "verify_aud": verify_aud,
                "require": ["exp", "iat", "jti", "iss", "sub", "permissions", "purpose"]
            }
            
            claims = jwt.decode(
                token,
                public_key_pem,
                algorithms=["EdDSA"],
                audience=audience if verify_aud and audience else None,
                options=options
            )
            
            # Additional AIF-specific validations
            self._validate_aif_claims(claims)
            
            logger.info(f"Token verified successfully. JTI: {claims.get('jti')}")
            return claims
            
        except jwt.ExpiredSignatureError:
            raise AIFSDKClientError("Token has expired")
        except jwt.InvalidAudienceError:
            raise AIFSDKClientError(f"Invalid audience. Expected: {audience}")
        except jwt.InvalidTokenError as e:
            raise AIFSDKClientError(f"Invalid token: {e}")
        except Exception as e:
            raise AIFSDKClientError(f"Token verification failed: {e}")
    
    def _validate_aif_claims(self, claims: Dict[str, Any]):
        """Validate AIF-specific claims."""
        # Check required AIF claims
        required_claims = ["permissions", "purpose"]
        for claim in required_claims:
            if claim not in claims:
                raise AIFSDKClientError(f"Missing required claim: {claim}")
        
        # Validate permissions format
        permissions = claims.get("permissions", [])
        if not isinstance(permissions, list) or not permissions:
            raise AIFSDKClientError("Invalid permissions claim")
        
        # Validate AID format in subject
        sub = claims.get("sub", "")
        if not sub or sub.count("/") < 3:
            raise AIFSDKClientError(f"Invalid AID format in subject: {sub}")

async def verify_token_with_revocation_check(
    client: 'AIFClient',
    token: str,
    audience: Optional[str] = None
) -> Dict[str, Any]:
    """
    Verify a token and check its revocation status.
    
    This is a convenience function that combines local verification
    with a revocation status check.
    
    Args:
        client: The AIFClient instance
        token: The JWT token to verify
        audience: Expected audience
        
    Returns:
        Dict containing verified claims
        
    Raises:
        AIFSDKClientError: If verification fails or token is revoked
    """
    # Get JWKS if not cached
    jwks = await client.get_jwks()
    
    # Create verifier
    verifier = TokenVerifier(jwks)
    
    # Verify token signature and claims
    claims = verifier.verify_token(token, audience=audience)
    
    # Check revocation status
    jti = claims.get("jti")
    if jti:
        is_revoked = await client.check_token_revocation_status(jti)
        if is_revoked:
            raise AIFSDKClientError(f"Token has been revoked. JTI: {jti}")
    
    return claims