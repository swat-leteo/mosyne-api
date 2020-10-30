"""
Users endpoints testing.
"""

# CONSTANTS
user_id = ""
user_email = ""


def test_create_test_user(client, user_mock):
    """POST /auth/signup."""

    user = user_mock.copy()
    response = client.post("/api/auth/signup", json=user)

    assert response.status_code == 201
    assert "detail" in response.json()

    global user_email
    user_email = user["email"]


def test_validate_email(client, get_token, user_mock):
    """POST /auth/make-verification."""

    token = get_token(user_email)
    response = client.get(f"/api/auth/make-verification?token={token}")
    assert "detail" in response.json()


def test_login(client, user_mock):
    """POST /auth/login."""

    credentials = {"email": user_email, "password": user_mock["password"]}
    response = client.post("/api/auth/login", json=credentials)

    assert response.status_code == 200

    global user_id
    user_id = response.json()["id"]


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


def test_get_current_user_unauthorized(client, get_token, app_settings):
    """GET /users. - 401"""

    token = get_token("invalid@invalid.com")
    response = client.get(
        "/api/users", cookies={f"{app_settings.COOKIE_SESSION_NAME}": token}
    )

    assert response.status_code == 401


def test_update_user(client, get_token, app_settings, profile_mock):
    """PUT /users. - 200"""

    token = get_token(user_email)
    profile_mock.update({"email": user_email})

    response = client.put(
        "/api/users",
        cookies={f"{app_settings.COOKIE_SESSION_NAME}": token},
        json=profile_mock,
    )
    body = response.json()

    assert response.status_code == 200
    assert body.get("id") == user_id
    assert body.get("address") == profile_mock["address"]


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


def test_delete_user(client, get_token, app_settings):
    """DELETE /users. - 200"""

    token = get_token(user_email)

    response = client.delete(
        "/api/users",
        cookies={f"{app_settings.COOKIE_SESSION_NAME}": token},
    )
    response.json()

    assert response.status_code == 200
    assert "detail" in response.json()


def test_delete_unauthorized(client, get_token, app_settings):
    """DELETE /users. - 401"""

    token = get_token("invalid@ginvalid.com")

    response = client.delete(
        "/api/users",
        cookies={f"{app_settings.COOKIE_SESSION_NAME}": token},
    )

    assert response.status_code == 401
