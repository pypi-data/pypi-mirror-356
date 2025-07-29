# Enhanced models.py with fixed Pydantic v2 field definitions

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Optional, Any
from datetime import datetime

class ATKIssuanceRequestData(BaseModel):
    """
    Data payload for requesting an ATK from the IE.
    Matches the AIF Core Service's ATKIssuanceRequest model.
    """
    user_id: str = Field(..., description="User identifier for delegation.", json_schema_extra={"example": "user-ab-001"})
    audience_sp_id: str = Field(..., description="Target SP audience.", json_schema_extra={"example": "https://sp.example.com/api"})
    permissions: List[str] = Field(..., min_length=1, description="Specific permissions granted.", json_schema_extra={"example": ["read:articles_all", "summarize:text_content_short"]})
    purpose: str = Field(..., description="Purpose of this token/agent task.", json_schema_extra={"example": "Daily news summary for user."})
    model_id: str = Field(..., description="AI model identifier used.", json_schema_extra={"example": "gpt-4-turbo"})
    override_trust_tags: Optional[Dict[str, str]] = Field(None, description="Optional trust metadata.", json_schema_extra={"example": {"user_verification_level": "platform_verified"}})

class IssuedATK(BaseModel):
    """
    Represents the ATK received from the IE.
    Matches the AIF Core Service's ATKIssuanceResponse model.
    """
    atk: str = Field(..., description="The signed Agent Token (ATK) as a JWT string.")

class ATKRevocationRequestData(BaseModel):
    """
    Data payload for revoking an ATK.
    Matches the AIF Core Service's ATKRevocationRequest model.
    """
    jti: str = Field(..., description="The JWT ID (jti claim) of the ATK to be revoked.")

class RevocationStatusResponse(BaseModel):
    """
    Response from checking token revocation status.
    """
    jti: str = Field(..., description="The JWT ID that was checked")
    is_revoked: bool = Field(..., description="Whether the token is revoked")
    checked_at: datetime = Field(..., description="When the check was performed")

class JWK(BaseModel):
    """
    JSON Web Key model.
    """
    kty: str = Field(..., description="Key type", json_schema_extra={"example": "OKP"})
    crv: str = Field(..., description="Curve name", json_schema_extra={"example": "Ed25519"})
    kid: str = Field(..., description="Key ID")
    x: str = Field(..., description="X coordinate (base64url)")
    alg: str = Field(..., description="Algorithm", json_schema_extra={"example": "EdDSA"})
    use: str = Field(..., description="Key use", json_schema_extra={"example": "sig"})

class JWKS(BaseModel):
    """
    JSON Web Key Set model.
    """
    keys: List[JWK] = Field(..., description="Array of JSON Web Keys")

class MessageResponse(BaseModel):
    """
    Generic message response from the service.
    """
    message: str = Field(..., description="Response message")
    detail: Optional[str] = Field(None, description="Additional details")
    status_code: Optional[int] = Field(None, description="HTTP status code")

class TokenClaims(BaseModel):
    """
    Decoded ATK claims for local validation.
    """
    iss: str = Field(..., description="Issuer")
    sub: str = Field(..., description="Subject (AID)")
    aud: str = Field(..., description="Audience")
    exp: int = Field(..., description="Expiration timestamp")
    iat: int = Field(..., description="Issued at timestamp")
    jti: str = Field(..., description="JWT ID")
    permissions: List[str] = Field(..., description="Granted permissions")
    purpose: str = Field(..., description="Token purpose")
    aif_trust_tags: Optional[Dict[str, str]] = Field(None, description="Trust metadata")

# Supported AI Models 
SUPPORTED_AI_MODELS = [
    "gpt-4-turbo",
    "gpt-3.5-turbo",
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "gemini-1.5-pro-latest",
    "meta-llama/Meta-Llama-3-70B-Instruct",
    "mistralai/Mistral-7B-Instruct-v0.2",
    "mistralai/Mixtral-8x7B-Instruct-v0.1",
    "command-r-plus",
    "HuggingFaceH4/zephyr-7b-alpha",
    "openchat/openchat-3.5-0106",
    "microsoft/phi-2"
]

# Standard Permissions 
STANDARD_PERMISSIONS = [
    "read:articles_all",
    "read:articles_topic_tech",
    "read:user_profile_basic",
    "summarize:text_content_short",
    "summarize:text_content_long",
    "analyze:sentiment_text",
    "interact:chatbot_basic",
    "kms:read_secret_group_A",
]

# Allowed Trust Tag Keys 
ALLOWED_TRUST_TAG_KEYS = [
    "user_verification_level",
    "issuer_assurance",
    "agent_environment",
    "data_processing_region"
]