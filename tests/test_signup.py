from urllib.parse import quote


def test_signup_adds_new_participant(client):
    # Arrange
    activity_name = "Chess Club"
    encoded_activity = quote(activity_name, safe="")
    new_email = "new.student@mergington.edu"
    before = client.get("/activities").json()[activity_name]["participants"]

    # Act
    response = client.post(
        f"/activities/{encoded_activity}/signup",
        params={"email": new_email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up {new_email} for {activity_name}",
    }
    after = client.get("/activities").json()[activity_name]["participants"]
    assert new_email not in before
    assert new_email in after


def test_signup_rejects_duplicate_participant(client):
    # Arrange
    activity_name = "Chess Club"
    encoded_activity = quote(activity_name, safe="")
    existing_email = "michael@mergington.edu"
    before = client.get("/activities").json()[activity_name]["participants"]

    # Act
    response = client.post(
        f"/activities/{encoded_activity}/signup",
        params={"email": existing_email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}
    after = client.get("/activities").json()[activity_name]["participants"]
    assert after == before
