"""
Users endpoints testing.
"""

# CONSTANTS
user_id = ""
user_email = ""


def test_create_test_user(client, user_mock):
    """POST /auth/signup."""

    response = client.post("/api/auth/signup", json=user_mock)
    body = response.json()

    assert response.status_code == 201
    assert body.get("email") == user_mock["email"]
    assert body.get("id") is not None

    body.get("id")
    user_mock["email"]


def test_complete_profile(client, get_token, profile_mock, app_settings):
    """POST /users."""

    token = get_token(user_email)
    response = client.post(
        "/api/users",
        cookies={f"{app_settings.COOKIE_SESSION_NAME}": token},
        json=profile_mock,
    )

    body = response.json()

    assert response.status_code == 201
    assert body.get("id") == user_id
    assert body.get("address") == profile_mock["address"]


def test_complete_profile_not_authenticated(client, profile_mock):
    """POST /users. - 403"""

    response = client.post("/api/users", json=profile_mock)
    assert response.status_code == 403


def test_complete_profile_unauthorized(client, get_token, profile_mock, app_settings):
    """POST /users.- 401"""

    token = get_token("invalid@gmail.invalid")
    response = client.post(
        "/api/users",
        cookies={f"{app_settings.COOKIE_SESSION_NAME}": token},
        json=profile_mock,
    )
    assert response.status_code == 401


def test_get_current_user(client, get_token, profile_mock, app_settings):
    """GET /users."""

    token = get_token(user_email)
    response = client.get(
        "/api/users", cookies={f"{app_settings.COOKIE_SESSION_NAME}": token}
    )

    body = response.json()

    assert response.status_code == 200
    assert body.get("id") == user_id
    assert body.get("email") == user_email
    assert body.get("address") == profile_mock["address"]


def test_get_current_user_unauthorized(client, get_token, app_settings):
    """GET /users. - 401"""

    token = get_token("invalid@invalid.com")
    response = client.get(
        "/api/users", cookies={f"{app_settings.COOKIE_SESSION_NAME}": token}
    )

    assert response.status_code == 401


def test_get_current_user_not_authenticated(client):
    """GET /users. - 403"""

    response = client.get("/api/users")
    assert response.status_code == 403


def test_update_user(client, get_token, app_settings):
    """PUT /users. - 200"""

    token = get_token(user_email)
    new_phone = "5523569752"

    response = client.put(
        "/api/users",
        cookies={f"{app_settings.COOKIE_SESSION_NAME}": token},
        json={"phone": new_phone},
    )
    body = response.json()

    assert response.status_code == 200
    assert body.get("id") == user_id
    assert body.get("phone") == new_phone


def test_update_user_unauthorized(client, get_token, app_settings):
    """PUT /users. - 401"""

    token = get_token("invalid@invalid.com")
    new_phone = "5523569752"

    response = client.put(
        "/api/users",
        cookies={f"{app_settings.COOKIE_SESSION_NAME}": token},
        json={"phone": new_phone},
    )

    assert response.status_code == 401


def test_update_user_not_authenticated(client, app_settings):
    """PUT /users. - 403"""

    new_phone = "5523569752"
    response = client.put(
        "/api/users",
        json={"phone": new_phone},
    )

    assert response.status_code == 403


def test_delete_user(client, get_token, app_settings):
    """DELETE /users. - 200"""

    token = get_token(user_email)

    response = client.delete(
        "/api/users",
        cookies={f"{app_settings.COOKIE_SESSION_NAME}": token},
    )
    body = response.json()

    assert response.status_code == 200
    assert body.get("detail") is not None


def test_delete_unauthorized(client, get_token, app_settings):
    """DELETE /users. - 401"""

    token = get_token("invalid@ginvalid.com")

    response = client.delete(
        "/api/users",
        cookies={f"{app_settings.COOKIE_SESSION_NAME}": token},
    )

    assert response.status_code == 401


def test_delete_not_authenticated(client):
    """DELETE /users. - 403"""

    get_token("invalid@ginvalid.com")
    response = client.delete("/api/users")

    assert response.status_code == 403
