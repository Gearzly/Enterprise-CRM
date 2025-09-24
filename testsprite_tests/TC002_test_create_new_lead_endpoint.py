import requests
import uuid

BASE_URL = "http://localhost:8000"
LEADS_ENDPOINT = f"{BASE_URL}/sales/leads"
TIMEOUT = 30
HEADERS = {'Content-Type': 'application/json'}

def test_create_new_lead_endpoint():
    # Construct a sample new lead payload
    new_lead_payload = {
        "name": f"Test Lead {uuid.uuid4()}",
        "email": f"testlead{uuid.uuid4().hex[:8]}@example.com",
        "phone": "+1234567890",
        "company": "Test Company",
        "source": "UnitTest",
        "status": "New",
        "notes": "Lead created during automated testing"
    }
    lead_id = None

    try:
        # Create a new lead
        response = requests.post(
            LEADS_ENDPOINT,
            json=new_lead_payload,
            headers=HEADERS,
            timeout=TIMEOUT
        )

        # Assert the response status code is 201 Created
        assert response.status_code == 201, f"Expected status code 201, got {response.status_code}"

        # Assert response content is JSON and contains confirmation (assuming returns lead id or similar)
        json_response = response.json()
        assert isinstance(json_response, dict), "Response is not a JSON object"

        # Assuming the created lead has an 'id' field in response
        assert 'id' in json_response, "Response JSON does not contain lead 'id'"

        lead_id = json_response["id"]
        assert lead_id is not None, "Lead id is None"

        # Additional possible confirmation checks
        # Optionally verify returned lead info matches sent payload (besides id)
        for key in ['name', 'email', 'phone', 'company', 'source', 'status', 'notes']:
            if key in json_response:
                assert json_response[key] == new_lead_payload[key], f"Mismatch in lead field '{key}'"

    finally:
        # Cleanup: Delete the created lead if lead_id is available
        if lead_id:
            delete_url = f"{LEADS_ENDPOINT}/{lead_id}"
            try:
                del_response = requests.delete(delete_url, timeout=TIMEOUT)
                # Accept 204 No Content or 200 OK as success for deletion
                assert del_response.status_code in [200, 204], f"Failed to delete lead with id {lead_id}, status code: {del_response.status_code}"
            except Exception as e:
                # Log or raise if deletion fails
                raise RuntimeError(f"Error during cleanup deleting lead with id {lead_id}: {str(e)}") from e

test_create_new_lead_endpoint()