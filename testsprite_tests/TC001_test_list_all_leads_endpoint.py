import requests

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

def test_list_all_leads_endpoint():
    url = f"{BASE_URL}/sales/leads"
    headers = {
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, timeout=TIMEOUT)
    except requests.RequestException as e:
        assert False, f"Request to {url} failed with exception: {e}"

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        leads = response.json()
    except ValueError:
        assert False, "Response is not valid JSON"

    # Validate that the response is a list (of leads)
    assert isinstance(leads, list), f"Expected response to be a list, got {type(leads)}"

    # If leads list is not empty, validate essential structure of each lead item
    if leads:
        lead = leads[0]
        # Common expected fields in a lead (guessing typical CRM lead fields)
        expected_fields = {"id", "name", "email", "phone", "status", "created_at"}
        assert isinstance(lead, dict), f"Expected lead to be a dict, got {type(lead)}"
        missing_fields = expected_fields - lead.keys()
        # It's possible that some fields may be optional, so check only common fields that likely exist
        assert not missing_fields, f"Lead object missing expected fields: {missing_fields}"

test_list_all_leads_endpoint()