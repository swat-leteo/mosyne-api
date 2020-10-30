"""
Users endpoints testing.
"""

from uuid import uuid4

# CONSTANTS
user_id = ""
user_email = ""
angel_id = ""
contact_id = ""


def test_setup_test_guardian(client, user_mock, get_token):
    """POST /auth/signup."""

    # Create the user/guardian
    response = client.post("/api/auth/signup", json=user_mock)
    assert response.status_code == 201
    assert "detail" in response.json()

    global user_email
    user_email = user_mock["email"]

    # Varified the user account
    token = get_token(user_email)
    response = client.get(f"/api/auth/make-verification?token={token}")
    assert "detail" in response.json()

    # Login the user
    credentials = {"email": user_email, "password": user_mock["password"]}
    response = client.post("/api/auth/login", json=credentials)
    assert response.status_code == 200

    global user_id
    user_id = response.json()["id"]


def test_create_angel(client, get_token, app_settings, angel_mock, user_mock):
    """POST /angels."""

    token = get_token(user_email)
    response = client.post(
        "/api/angels?use_guardian_address=true",
        json=angel_mock,
        cookies={f"{app_settings.COOKIE_SESSION_NAME}": token},
    )

    body = response.json()

    assert response.status_code == 201
    assert "id" in body
    assert "id" in body["contacts"][0]

    angel_mock["contacts"][0]["id"] = body["contacts"][0]["id"]
    assert body["contacts"] == angel_mock["contacts"]

    global angel_id
    global contact_id
    angel_id = body["id"]
    contact_id = body["contacts"][0]["id"]


def test_create_angel_unauthorized(client, get_token, app_settings, angel_mock):
    """POST /angels. - 401"""

    token = get_token("invalid@invalid.com")
    response = client.post(
        "/api/angels?use_guardian_address=true",
        json=angel_mock,
        cookies={f"{app_settings.COOKIE_SESSION_NAME}": token},
    )

    assert response.status_code == 401


def test_get_all_angels(client, get_token, app_settings):
    """GET /angels."""

    token = get_token(user_email)
    response = client.get(
        "/api/angels",
        cookies={f"{app_settings.COOKIE_SESSION_NAME}": token},
    )

    body = response.json()

    assert response.status_code == 200
    assert len(body) == 1
    assert body[0]["id"] == angel_id


def test_get_all_angels_unauthorized(client, get_token, app_settings):
    """GET /angels. - 401"""

    token = get_token("invalid@invalid.com")
    response = client.get(
        "/api/angels",
        cookies={f"{app_settings.COOKIE_SESSION_NAME}": token},
    )

    assert response.status_code == 401


def test_get_angel(client):
    """GET /angels/{id}."""

    response = client.get(f"/api/angels/{angel_id}")

    body = response.json()
    assert response.status_code == 200
    assert body["id"] == angel_id


def test_get_angel_invalid_request(client):
    """GET /angels/{id}. - 422"""

    invalid_id = "someInvalidID"
    response = client.get(f"/api/angels/{invalid_id}")

    assert response.status_code == 422


def test_update_angel(client, get_token, app_settings, angel_update_mock):
    """PUT /angels."""

    token = get_token(user_email)
    response = client.put(
        f"/api/angels/{angel_id}",
        json=angel_update_mock,
        cookies={f"{app_settings.COOKIE_SESSION_NAME}": token},
    )

    body = response.json()

    assert response.status_code == 200
    assert body["id"] == angel_id
    assert body["surgeries"] == angel_update_mock["surgeries"]


def test_update_angel_unauthorized(client, get_token, app_settings, angel_update_mock):
    """PUT /angels. - 401"""

    token = get_token("invalid@invalid.com")
    response = client.put(
        f"/api/angels/{angel_id}",
        json=angel_update_mock,
        cookies={f"{app_settings.COOKIE_SESSION_NAME}": token},
    )

    assert response.status_code == 401


def test_update_angel(client, get_token, app_settings, angel_update_mock):
    """PUT /angels. - 404"""

    token = get_token(user_email)
    response = client.put(
        f"/api/angels/{uuid4()}",
        json=angel_update_mock,
        cookies={f"{app_settings.COOKIE_SESSION_NAME}": token},
    )

    assert response.status_code == 404


def test_get_qr(client, get_token, app_settings):
    """GET /angels/{id}/qr."""

    token = get_token(user_email)
    response = client.get(
        f"/api/angels/{angel_id}/qr",
        cookies={f"{app_settings.COOKIE_SESSION_NAME}": token},
    )

    assert response.status_code == 200
    assert "qr_image" in response.json()
    assert response.json()["qr_image"].startswith("data:image/png;base64,")


def test_get_qr_unauthorized(client, get_token, app_settings):
    """GET /angels/{id}/qr. - 401"""

    token = get_token("invalid@invalid.com")
    response = client.get(
        f"/api/angels/{angel_id}/qr",
        cookies={f"{app_settings.COOKIE_SESSION_NAME}": token},
    )
    assert response.status_code == 401


def test_update_contact(client, get_token, app_settings, angel_mock):
    """PUT /angels/contacts/{id}."""

    token = get_token(user_email)
    contact = angel_mock["contacts"][0]
    contact["cel"] = "+5254858639"
    response = client.put(
        f"/api/angels/contact/{contact_id}",
        json=contact,
        cookies={f"{app_settings.COOKIE_SESSION_NAME}": token},
    )
    body = response.json()

    assert response.status_code == 200
    assert body["id"] == angel_id
    assert body["contacts"][0]["id"] == contact_id


def test_delete_agel_unauthorized(client, get_token, app_settings):
    """DELETE /angels - 401"""

    token = get_token("invalid@invalid.com")
    response = client.delete(
        f"/api/angels/{angel_id}",
        cookies={f"{app_settings.COOKIE_SESSION_NAME}": token},
    )

    assert response.status_code == 401


def test_delete_agel(client, get_token, app_settings):
    """DELETE /angels"""

    token = get_token(user_email)
    response = client.delete(
        f"/api/angels/{angel_id}",
        cookies={f"{app_settings.COOKIE_SESSION_NAME}": token},
    )

    assert response.status_code == 200
    assert "detail" in response.json()


def test_delete_agel_not_found(client, get_token, app_settings):
    """DELETE /angels. - 404"""

    token = get_token(user_email)
    response = client.delete(
        f"/api/angels/{angel_id}",
        cookies={f"{app_settings.COOKIE_SESSION_NAME}": token},
    )

    assert response.status_code == 404
