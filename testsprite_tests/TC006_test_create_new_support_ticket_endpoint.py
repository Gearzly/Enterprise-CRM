import requests

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

def test_create_new_support_ticket_endpoint():
    url = f"{BASE_URL}/support/tickets"
    headers = {
        "Content-Type": "application/json"
    }
    # Example payload for a support ticket creation based on typical support ticket fields
    payload = {
        "title": "Test Ticket Creation",
        "description": "This is a test ticket created during automated testing.",
        "priority": "normal",  # typically low, normal, high or urgent
        "status": "open"       # initial status
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=TIMEOUT)
    except requests.RequestException as e:
        assert False, f"Request failed: {e}"

    assert response.status_code == 201, f"Expected status code 201, got {response.status_code}"
    try:
        data = response.json()
    except ValueError:
        assert False, "Response is not valid JSON"

    # Check confirmation fields in response (e.g. id or message)
    assert "id" in data or "ticket_id" in data or "message" in data, "Response JSON missing confirmation content"

test_create_new_support_ticket_endpoint()
