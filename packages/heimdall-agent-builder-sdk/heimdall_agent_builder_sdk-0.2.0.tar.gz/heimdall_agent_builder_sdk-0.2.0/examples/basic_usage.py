# examples/basic_usage.py
"""
Example usage of the AIF Agent Builder SDK.
"""

import asyncio
import os
from typing import Optional
from aif_agent_builder_sdk import (
    AIFClient, 
    AIFSDKClientError, 
    AIFServiceError,
    SUPPORTED_AI_MODELS,
    STANDARD_PERMISSIONS
)

# Load environment variables (optional if using .env file)
from dotenv import load_dotenv
load_dotenv()

async def basic_token_lifecycle():
    """Demonstrates the basic token lifecycle: issue, use, check, revoke."""
    
    # Initialize the client
    client = AIFClient(
        core_service_url="http://localhost:5000",
        issuer_api_key=os.getenv("AIF_SDK_ISSUER_API_KEY")
    )
    
    try:
        # 1. Request an ATK
        print("1. Requesting Agent Token...")
        issued_token = await client.request_aif_token(
            user_id="user-123",
            audience_sp_id="https://news-api.example.com",
            permissions=["read:articles_all", "summarize:text_content_short"],
            purpose="Summarize today's tech news for the user",
            model_id="gpt-4-turbo",
            override_trust_tags={
                "user_verification_level": "email_verified",
                "agent_environment": "production"
            }
        )
        print(f"   ✅ Token issued successfully!")
        print(f"   Token (first 50 chars): {issued_token.atk[:50]}...")
        
        # 2. Validate token locally (basic checks)
        print("\n2. Validating token locally...")
        claims = await client.validate_token_locally(issued_token.atk)
        print(f"   Subject (AID): {claims['sub']}")
        print(f"   Audience: {claims['aud']}")
        print(f"   Permissions: {claims['permissions']}")
        print(f"   JTI: {claims['jti']}")
        
        # 3. Get JWKS (for signature verification)
        print("\n3. Fetching JWKS...")
        jwks = await client.get_jwks()
        print(f"   Found {len(jwks['keys'])} key(s)")
        print(f"   Key ID: {jwks['keys'][0]['kid']}")
        
        # 4. Check revocation status
        print("\n4. Checking revocation status...")
        is_revoked = await client.check_token_revocation_status(claims['jti'])
        print(f"   Is revoked: {is_revoked}")
        
        # 5. Use the token in a request (example)
        print("\n5. Using token in API request...")
        auth_header = AIFClient.get_aif_authorization_header(issued_token)
        print(f"   Authorization header: {auth_header}")
        
        # 6. Revoke the token
        print("\n6. Revoking token...")
        revoke_response = await client.revoke_aif_token(claims['jti'])
        print(f"   {revoke_response['message']}")
        
        # 7. Verify revocation
        print("\n7. Verifying revocation...")
        is_revoked_after = await client.check_token_revocation_status(claims['jti'])
        print(f"   Is revoked now: {is_revoked_after}")
        
    except AIFServiceError as e:
        print(f"❌ Service error: {e}")
        print(f"   Status code: {e.status_code}")
        print(f"   Detail: {e.detail}")
    except AIFSDKClientError as e:
        print(f"❌ Client error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        await client.close()

async def context_manager_example():
    """Demonstrates using the client as a context manager."""
    
    async with AIFClient() as client:
        # The client will automatically close when exiting the context
        
        # Get JWKS
        jwks = await client.get_jwks()
        print(f"JWKS has {len(jwks['keys'])} keys")
        
        # Issue a token
        token = await client.request_aif_token(
            user_id="user-456",
            audience_sp_id="https://api.example.com",
            permissions=["read:user_profile_basic"],
            purpose="Display user profile",
            model_id="gpt-3.5-turbo"
        )
        print(f"Token issued with JTI: {(await client.validate_token_locally(token.atk))['jti']}")

async def batch_operations_example():
    """Example of handling multiple token operations efficiently."""
    
    async with AIFClient() as client:
        # Issue multiple tokens concurrently
        token_requests = [
            client.request_aif_token(
                user_id=f"user-{i}",
                audience_sp_id="https://api.example.com",
                permissions=["read:articles_all"],
                purpose=f"Task {i}",
                model_id="gpt-4-turbo"
            )
            for i in range(3)
        ]
        
        # Wait for all tokens to be issued
        tokens = await asyncio.gather(*token_requests)
        print(f"Issued {len(tokens)} tokens")
        
        # Check revocation status for all tokens
        jtis = [(await client.validate_token_locally(t.atk))['jti'] for t in tokens]
        
        revocation_checks = [
            client.check_token_revocation_status(jti) 
            for jti in jtis
        ]
        
        statuses = await asyncio.gather(*revocation_checks)
        print(f"Revocation statuses: {statuses}")

async def error_handling_example():
    """Demonstrates proper error handling."""
    
    client = AIFClient()
    
    try:
        # Try with invalid permissions
        token = await client.request_aif_token(
            user_id="user-789",
            audience_sp_id="https://api.example.com",
            permissions=[],  # Empty permissions list
            purpose="Test",
            model_id="invalid-model"
        )
    except AIFServiceError as e:
        print(f"Expected service error: {e}")
    
    try:
        # Try with invalid token for revocation
        await client.revoke_aif_token("invalid-jti")
    except AIFServiceError as e:
        print(f"Revocation error: {e}")
    
    finally:
        await client.close()

def print_supported_resources():
    """Print supported AI models and permissions."""
    print("Supported AI Models:")
    for model in SUPPORTED_AI_MODELS:
        print(f"  - {model}")
    
    print("\nStandard Permissions:")
    for perm in STANDARD_PERMISSIONS:
        print(f"  - {perm}")

if __name__ == "__main__":
    # Print supported resources
    print_supported_resources()
    print("\n" + "="*50 + "\n")
    
    # Run examples
    print("Running basic token lifecycle example...")
    asyncio.run(basic_token_lifecycle())
    
    print("\n" + "="*50 + "\n")
    print("Running context manager example...")
    asyncio.run(context_manager_example())
    
    print("\n" + "="*50 + "\n")
    print("Running batch operations example...")
    asyncio.run(batch_operations_example())
    
    print("\n" + "="*50 + "\n")
    print("Running error handling example...")
    asyncio.run(error_handling_example())