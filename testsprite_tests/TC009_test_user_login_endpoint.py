import requests

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

def test_user_login_endpoint():
    url = f"{BASE_URL}/auth/login"
    headers = {"Content-Type": "application/json"}

    # Valid credentials (these should be replaced with actual valid test credentials)
    valid_credentials = {
        "username": "testuser",
        "password": "TestPassword123!"
    }

    # Invalid credentials
    invalid_credentials = {
        "username": "testuser",
        "password": "WrongPassword!"
    }

    # Test login with valid credentials
    try:
        response = requests.post(url, json=valid_credentials, headers=headers, timeout=TIMEOUT)
    except requests.RequestException as e:
        assert False, f"Request failed for valid credentials: {e}"
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code} for valid credentials"
    try:
        json_data = response.json()
    except ValueError:
        assert False, "Response body is not valid JSON for valid credentials login"
    assert "token" in json_data and isinstance(json_data["token"], str) and len(json_data["token"]) > 0, "Token not found or invalid in response for valid credentials"

    # Test login with invalid credentials
    try:
        response = requests.post(url, json=invalid_credentials, headers=headers, timeout=TIMEOUT)
    except requests.RequestException as e:
        assert False, f"Request failed for invalid credentials: {e}"
    assert response.status_code == 401, f"Expected status code 401 but got {response.status_code} for invalid credentials"

test_user_login_endpoint()