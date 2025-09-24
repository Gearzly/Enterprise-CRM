import requests
import uuid

BASE_URL = "http://localhost:8000"
TIMEOUT = 30
HEADERS = {
    "Content-Type": "application/json",
    # Add Authorization header here if authentication is required, e.g.:
    # "Authorization": "Bearer <token>"
}

def test_create_new_campaign_endpoint():
    campaign_url = f"{BASE_URL}/marketing/campaigns"
    # Sample payload for creating a new marketing campaign
    payload = {
        "name": f"Test Campaign {uuid.uuid4()}",
        "description": "This is a test campaign created during automated testing.",
        "start_date": "2025-10-01",
        "end_date": "2025-12-31",
        "budget": 10000.00,
        "status": "planned",
        "channels": ["email", "social_media"]
    }

    created_campaign_id = None

    try:
        response = requests.post(campaign_url, json=payload, headers=HEADERS, timeout=TIMEOUT)
        # Assert status code
        assert response.status_code == 201, f"Expected status code 201, got {response.status_code}"
        
        # Assert response content-type
        content_type = response.headers.get("Content-Type", "")
        assert "application/json" in content_type.lower(), f"Expected JSON response, got {content_type}"
        
        response_json = response.json()
        
        # Validate that response includes confirmation fields
        assert "id" in response_json, "Response JSON must contain 'id' field for the created campaign"
        assert response_json.get("name") == payload["name"], "Campaign name in response does not match payload"
        
        created_campaign_id = response_json["id"]

    finally:
        # Clean up: delete the created campaign if created_campaign_id is set
        if created_campaign_id:
            delete_url = f"{campaign_url}/{created_campaign_id}"
            try:
                del_response = requests.delete(delete_url, headers=HEADERS, timeout=TIMEOUT)
                # Acceptable to delete 200 or 204; silently ignore failure to not mask the test result
                if del_response.status_code not in (200, 204):
                    print(f"Warning: Failed to delete campaign id {created_campaign_id}, status code {del_response.status_code}")
            except Exception as e:
                print(f"Warning: Exception during cleanup deleting campaign id {created_campaign_id}: {e}")

test_create_new_campaign_endpoint()