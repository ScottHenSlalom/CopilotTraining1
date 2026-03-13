from urllib.parse import quote


def test_unregister_removes_existing_participant(client):
    # Arrange
    activity_name = "Chess Club"
    encoded_activity = quote(activity_name, safe="")
    existing_email = "michael@mergington.edu"
    before = client.get("/activities").json()[activity_name]["participants"]

    # Act
    response = client.delete(
        f"/activities/{encoded_activity}/signup",
        params={"email": existing_email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Unregistered {existing_email} from {activity_name}",
    }
    after = client.get("/activities").json()[activity_name]["participants"]
    assert existing_email in before
    assert existing_email not in after


def test_unregister_rejects_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    encoded_activity = quote(activity_name, safe="")
    email = "student@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{encoded_activity}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_rejects_student_not_signed_up(client):
    # Arrange
    activity_name = "Chess Club"
    encoded_activity = quote(activity_name, safe="")
    email = "not.registered@mergington.edu"
    before = client.get("/activities").json()[activity_name]["participants"]

    # Act
    response = client.delete(
        f"/activities/{encoded_activity}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Student is not signed up for this activity"}
    after = client.get("/activities").json()[activity_name]["participants"]
    assert after == before
