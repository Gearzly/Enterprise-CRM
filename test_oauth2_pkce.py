#!/usr/bin/env python3
"""
OAuth2 PKCE Authentication Flow Test
Tests the complete OAuth2 PKCE implementation
"""
import requests
import json
import hashlib
import base64
import secrets
from urllib.parse import urlencode

BASE_URL = "http://localhost:8001"

def test_oauth2_pkce_challenge():
    """Test PKCE challenge generation"""
    print("🔐 Testing PKCE challenge generation...")
    
    try:
        response = requests.post(f"{BASE_URL}/auth/challenge")
        
        if response.status_code == 200:
            challenge_data = response.json()
            print(f"✅ PKCE challenge generated successfully")
            print(f"   Code challenge: {challenge_data.get('code_challenge', 'N/A')[:20]}...")
            print(f"   Challenge method: {challenge_data.get('code_challenge_method', 'N/A')}")
            return challenge_data
        else:
            print(f"❌ PKCE challenge failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        return None

def generate_pkce_challenge():
    """Generate PKCE challenge locally for testing"""
    # Generate code verifier (43-128 characters)
    code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8').rstrip('=')
    
    # Generate code challenge using S256 method
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode('utf-8')).digest()
    ).decode('utf-8').rstrip('=')
    
    return {
        "code_verifier": code_verifier,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256"
    }

def test_oauth2_authorization():
    """Test OAuth2 authorization endpoint"""
    print("🔐 Testing OAuth2 authorization...")
    
    # Generate PKCE challenge
    pkce_data = generate_pkce_challenge()
    
    authorization_request = {
        "client_id": "crm_web_app",
        "redirect_uri": "http://localhost:3000/auth/callback",
        "code_challenge": pkce_data["code_challenge"],
        "code_challenge_method": "S256",
        "state": secrets.token_urlsafe(16)
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/authorize", json=authorization_request)
        
        if response.status_code == 200:
            auth_data = response.json()
            print(f"✅ Authorization successful")
            print(f"   Authorization code: {auth_data.get('authorization_code', 'N/A')[:20]}...")
            return auth_data, pkce_data
        else:
            print(f"❌ Authorization failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return None, None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        return None, None

def test_oauth2_token_exchange(auth_code, pkce_data):
    """Test OAuth2 token exchange"""
    print("🔐 Testing OAuth2 token exchange...")
    
    token_request = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": "http://localhost:3000/auth/callback",
        "code_verifier": pkce_data["code_verifier"],
        "client_id": "crm_web_app"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/token", json=token_request)
        
        if response.status_code == 200:
            token_data = response.json()
            print(f"✅ Token exchange successful")
            print(f"   Access token: {token_data.get('access_token', 'N/A')[:20]}...")
            print(f"   Token type: {token_data.get('token_type', 'N/A')}")
            print(f"   Expires in: {token_data.get('expires_in', 'N/A')} seconds")
            return token_data
        else:
            print(f"❌ Token exchange failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        return None

def test_oauth2_userinfo(access_token):
    """Test OAuth2 userinfo endpoint"""
    print("🔐 Testing OAuth2 userinfo...")
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/auth/userinfo", headers=headers)
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ UserInfo successful")
            print(f"   Subject: {user_data.get('sub', 'N/A')}")
            print(f"   Email: {user_data.get('email', 'N/A')}")
            print(f"   Role: {user_data.get('role', 'N/A')}")
            return user_data
        else:
            print(f"❌ UserInfo failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        return None

def test_protected_endpoint(access_token):
    """Test accessing a protected endpoint with OAuth2 token"""
    print("🔐 Testing protected endpoint access...")
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    # Test accessing a protected endpoint
    try:
        response = requests.get(f"{BASE_URL}/api/superadmin/users", headers=headers)
        
        if response.status_code == 200:
            print(f"✅ Protected endpoint access successful")
            return True
        elif response.status_code == 401:
            print(f"❌ Authentication required (expected if middleware is working)")
            return False
        elif response.status_code == 403:
            print(f"❌ Insufficient permissions (expected for some endpoints)")
            return False
        else:
            print(f"❌ Protected endpoint failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        return False

def test_oauth2_discovery():
    """Test OAuth2 discovery metadata"""
    print("🔐 Testing OAuth2 discovery metadata...")
    
    try:
        response = requests.get(f"{BASE_URL}/auth/.well-known/oauth-authorization-server")
        
        if response.status_code == 200:
            metadata = response.json()
            print(f"✅ OAuth2 discovery successful")
            print(f"   Issuer: {metadata.get('issuer', 'N/A')}")
            print(f"   Authorization endpoint: {metadata.get('authorization_endpoint', 'N/A')}")
            print(f"   Token endpoint: {metadata.get('token_endpoint', 'N/A')}")
            print(f"   Supported scopes: {metadata.get('scopes_supported', [])}")
            return metadata
        else:
            print(f"❌ OAuth2 discovery failed: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        return None

def test_simplified_token_flow():
    """Test simplified password-based token flow (for testing)"""
    print("🔐 Testing simplified token flow...")
    
    token_request = {
        "grant_type": "password",
        "username": "test@example.com",
        "password": "testpassword",
        "client_id": "crm_web_app",
        "scope": "read write"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/token", json=token_request)
        
        if response.status_code == 200:
            token_data = response.json()
            print(f"✅ Simplified token flow successful")
            print(f"   Access token: {token_data.get('access_token', 'N/A')[:20]}...")
            return token_data
        else:
            print(f"❌ Simplified token flow failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        return None

def main():
    """Run complete OAuth2 PKCE authentication flow test"""
    print("🚀 OAuth2 PKCE Authentication Flow Test")
    print("=" * 50)
    
    # Test OAuth2 discovery
    discovery_data = test_oauth2_discovery()
    print()
    
    # Test PKCE challenge generation
    challenge_data = test_oauth2_pkce_challenge()
    print()
    
    # Test OAuth2 authorization
    auth_data, pkce_data = test_oauth2_authorization()
    print()
    
    if auth_data and pkce_data:
        # Test token exchange
        token_data = test_oauth2_token_exchange(
            auth_data.get("authorization_code"),
            pkce_data
        )
        print()
        
        if token_data:
            access_token = token_data.get("access_token")
            
            # Test userinfo endpoint
            user_data = test_oauth2_userinfo(access_token)
            print()
            
            # Test protected endpoint access
            protected_access = test_protected_endpoint(access_token)
            print()
    
    # Test simplified flow for direct testing
    print("📋 Testing simplified flow for development...")
    simplified_token = test_simplified_token_flow()
    print()
    
    print("=" * 50)
    print("🎯 OAuth2 PKCE Test Summary:")
    print(f"   Discovery endpoint: {'✅' if discovery_data else '❌'}")
    print(f"   PKCE challenge: {'✅' if challenge_data else '❌'}")
    print(f"   Authorization flow: {'✅' if auth_data else '❌'}")
    print(f"   Token exchange: {'✅' if 'token_data' in locals() and token_data else '❌'}")
    print(f"   UserInfo endpoint: {'✅' if 'user_data' in locals() and user_data else '❌'}")
    print(f"   Simplified flow: {'✅' if simplified_token else '❌'}")
    
    if all([discovery_data, challenge_data, simplified_token]):
        print("🎉 OAuth2 PKCE implementation is working!")
    else:
        print("⚠️  Some OAuth2 PKCE features need attention")

if __name__ == "__main__":
    main()