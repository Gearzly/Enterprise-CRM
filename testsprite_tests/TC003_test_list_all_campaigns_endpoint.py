import requests

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

def test_list_all_campaigns_endpoint():
    url = f"{BASE_URL}/marketing/campaigns"
    headers = {
        "Accept": "application/json"
    }
    try:
        response = requests.get(url, headers=headers, timeout=TIMEOUT)
    except requests.RequestException as e:
        assert False, f"Request to {url} failed: {e}"

    # Validate status code
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    # Validate content type header
    content_type = response.headers.get("Content-Type", "")
    assert "application/json" in content_type, f"Unexpected content type: {content_type}"

    try:
        data = response.json()
    except ValueError:
        assert False, "Response is not valid JSON"

    # Validate data structure: expected a list (array) of campaigns
    assert isinstance(data, list), f"Expected response data to be a list but got {type(data)}"

    # If there are campaigns returned, validate structure of first item (optional deeper check)
    if data:
        campaign = data[0]
        assert isinstance(campaign, dict), "Each campaign should be a dict"
        # Basic fields that a campaign might have based on marketing context
        # Since schema details not fully provided, checking common fields presence
        expected_fields = ["id", "name", "status"]
        for field in expected_fields:
            assert field in campaign, f"Campaign missing expected field: {field}"

test_list_all_campaigns_endpoint()
