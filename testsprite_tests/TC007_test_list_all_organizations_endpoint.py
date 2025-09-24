import requests

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

def test_list_all_organizations_endpoint():
    url = f"{BASE_URL}/api/superadmin/organizations"
    headers = {
        "Accept": "application/json",
    }
    try:
        response = requests.get(url, headers=headers, timeout=TIMEOUT)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        assert False, f"Request to {url} failed: {e}"

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        assert False, "Response content is not valid JSON"

    # Assert that data is a list
    assert isinstance(data, list), f"Expected response to be a list, got {type(data)}"

    # If list not empty, check structure of first element
    if data:
        org = data[0]
        assert isinstance(org, dict), f"Expected each organization to be a dict, got {type(org)}"
        # Minimal expected keys (guessed typical organization fields)
        expected_keys = {"id", "name", "created_at", "updated_at"}
        org_keys = set(org.keys())
        missing_keys = expected_keys - org_keys
        assert not missing_keys, f"Organization dict missing keys: {missing_keys}"

test_list_all_organizations_endpoint()