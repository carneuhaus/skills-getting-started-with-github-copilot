from urllib.parse import quote


def _signup_path(activity_name: str) -> str:
    return f"/activities/{quote(activity_name)}/signup"


def test_root_redirects_to_static_index(client):
    # Arrange
    path = "/"

    # Act
    response = client.get(path, follow_redirects=False)

    # Assert
    assert response.status_code in (302, 307)
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_seeded_data(client):
    # Arrange
    path = "/activities"

    # Act
    response = client.get(path)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_success_adds_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    path = _signup_path(activity)
    params = {"email": email}

    # Act
    response = client.post(path, params=params)
    activities_response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity}"}

    activities = activities_response.json()
    assert email in activities[activity]["participants"]


def test_signup_duplicate_returns_400(client):
    # Arrange
    path = _signup_path("Chess Club")
    params = {"email": "michael@mergington.edu"}

    # Act
    response = client.post(path, params=params)

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_unknown_activity_returns_404(client):
    # Arrange
    path = _signup_path("Unknown Activity")
    params = {"email": "student@mergington.edu"}

    # Act
    response = client.post(path, params=params)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_without_email_returns_422(client):
    # Arrange
    path = _signup_path("Chess Club")

    # Act
    response = client.post(path)

    # Assert
    assert response.status_code == 422


def test_unregister_success_removes_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "daniel@mergington.edu"
    path = _signup_path(activity)
    params = {"email": email}

    # Act
    response = client.delete(path, params=params)
    activities_response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity}"}

    activities = activities_response.json()
    assert email not in activities[activity]["participants"]


def test_unregister_unknown_activity_returns_404(client):
    # Arrange
    path = _signup_path("Unknown Activity")
    params = {"email": "student@mergington.edu"}

    # Act
    response = client.delete(path, params=params)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_not_registered_returns_404(client):
    # Arrange
    path = _signup_path("Chess Club")
    params = {"email": "notregistered@mergington.edu"}

    # Act
    response = client.delete(path, params=params)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not registered for this activity"


def test_unregister_without_email_returns_422(client):
    # Arrange
    path = _signup_path("Chess Club")

    # Act
    response = client.delete(path)

    # Assert
    assert response.status_code == 422
