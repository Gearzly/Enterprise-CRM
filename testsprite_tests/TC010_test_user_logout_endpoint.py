import requests

BASE_URL = "http://localhost:8000"
LOGIN_ENDPOINT = f"{BASE_URL}/auth/login"
LOGOUT_ENDPOINT = f"{BASE_URL}/auth/logout"
TIMEOUT = 30

def test_user_logout_endpoint():
    # Sample valid user credentials for login (assumed for test)
    login_payload = {
        "username": "testuser",
        "password": "testpassword"
    }
    headers = {"Content-Type": "application/json"}

    # Authenticate user to obtain token for logout
    try:
        login_response = requests.post(LOGIN_ENDPOINT, json=login_payload, headers=headers, timeout=TIMEOUT)
        assert login_response.status_code == 200, f"Login failed with status code {login_response.status_code}"
        token = login_response.json().get("access_token")
        assert token, "Login response missing access_token"

        # Logout using the token in Authorization header
        logout_headers = {
            "Authorization": f"Bearer {token}"
        }
        logout_response = requests.post(LOGOUT_ENDPOINT, headers=logout_headers, timeout=TIMEOUT)

        # Assert logout success
        assert logout_response.status_code == 200, f"Logout failed with status code {logout_response.status_code}"
        logout_json = logout_response.json() if logout_response.content else {}
        # Optional: check message or confirmation in logout_json if present
    except requests.RequestException as e:
        assert False, f"Request failed: {e}"

test_user_logout_endpoint()