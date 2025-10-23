from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    # should return the activities mapping
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    activity = "Chess Club"
    email = "test_student@mergington.edu"

    # ensure clean state: remove if exists
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # signup
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]

    # duplicate signup should fail
    resp_dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp_dup.status_code == 400

    # unregister
    resp_un = client.post(f"/activities/{activity}/unregister?email={email}")
    assert resp_un.status_code == 200
    assert email not in activities[activity]["participants"]

    # unregistering again should fail
    resp_un2 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert resp_un2.status_code == 400


def test_signup_invalid_activity():
    resp = client.post("/activities/Nonexistent/signup?email=foo@bar.com")
    assert resp.status_code == 404


def test_unregister_invalid_activity():
    resp = client.post("/activities/Nonexistent/unregister?email=foo@bar.com")
    assert resp.status_code == 404
