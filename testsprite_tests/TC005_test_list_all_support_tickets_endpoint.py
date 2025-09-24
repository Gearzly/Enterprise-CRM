import requests

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

def test_list_all_support_tickets_endpoint():
    url = f"{BASE_URL}/support/tickets"
    headers = {
        "Accept": "application/json"
    }
    try:
        response = requests.get(url, headers=headers, timeout=TIMEOUT)
    except requests.RequestException as e:
        assert False, f"HTTP request failed: {e}"

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        assert False, "Response is not a valid JSON"

    # Validate that data is a list
    assert isinstance(data, list), f"Expected response data to be a list, got {type(data)}"

    # Validate data structure: each item should be a dict with at least expected keys
    # Since schema not detailed, check for typical support ticket fields existence if any
    # Common fields might be: id, subject, status, created_at, but we can't assume,
    # so we will check that each item is a dict.
    for item in data:
        assert isinstance(item, dict), f"Expected each ticket to be a dict, got {type(item)}"
        # Optionally check minimal keys if known:
        # assert "id" in item, "Ticket missing 'id' field"
        # assert "subject" in item, "Ticket missing 'subject' field"
        # If no fields known, skip.

test_list_all_support_tickets_endpoint()