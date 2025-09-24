import requests
import uuid

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

def test_create_new_organization_endpoint():
    url = f"{BASE_URL}/api/superadmin/organizations"
    headers = {
        "Content-Type": "application/json"
    }
    # Unique organization name to prevent conflicts
    org_name = f"TestOrg-{uuid.uuid4()}"
    payload = {
        "name": org_name,
        "description": "Organization created during automated test TC008",
        "address": "123 Test St, Test City, TS",
        "email": f"contact@{org_name.lower()}.com",
        "phone": "+1234567890"
    }

    created_org_id = None

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=TIMEOUT)
        assert response.status_code == 201, f"Expected status code 201, got {response.status_code}"
        response_json = response.json()
        # Confirm confirmation markers in response: typically the created resource or message
        assert "id" in response_json, "Response JSON does not contain 'id'"
        created_org_id = response_json["id"]
        assert isinstance(created_org_id, int) or isinstance(created_org_id, str), "Organization ID is not valid"
        # Optionally check name matches
        assert response_json.get("name") == org_name, "Organization name in response does not match payload"

    finally:
        # Cleanup: delete the created organization if creation succeeded
        if created_org_id:
            try:
                delete_url = f"{url}/{created_org_id}"
                del_response = requests.delete(delete_url, headers=headers, timeout=TIMEOUT)
                # Accept 200 or 204 as successful deletion
                assert del_response.status_code in (200, 204), f"Cleanup failed, deletion status code: {del_response.status_code}"
            except Exception as e:
                # Log cleanup failure, do not raise to hide original test results
                print(f"Cleanup error for organization id {created_org_id}: {e}")

test_create_new_organization_endpoint()
