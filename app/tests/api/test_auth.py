"""
Auth endpoints testing.
"""

# CONSTANTS
user_email = ""


def test_create_user(client, user_mock):
    """POST /auth/signup. 201"""

    user = user_mock.copy()
    response = client.post("/api/auth/signup", json=user)

    assert response.status_code == 201
    assert "detail" in response.json()

    global user_email
    user_email = user["email"]


def test_create_user_coflict(client, user_mock):
    """POST /auth/signup. 409"""

    user = user_mock.copy()
    user.update({"email": user_email})
    response = client.post("/api/auth/signup", json=user)

    assert response.status_code == 409
    assert "detail" in response.json()


def test_validate_email(client, get_token, user_mock):
    """POST /auth/make-verification. - 200"""

    token = get_token(user_email)
    response = client.get(f"/api/auth/make-verification?token={token}")
    assert "detail" in response.json()


def test_validate_email_invalid(client, get_token, user_mock):
    """POST /auth/make-verification. - 404"""

    token = get_token(user_email)
    response = client.get(f"/api/auth/make-verification?token={token}")

    assert response.status_code == 404
    assert "detail" in response.json()


def test_login(client, user_mock):
    """POST /auth/login. - 200"""

    credentials = {"email": user_email, "password": user_mock["password"]}
    response = client.post("/api/auth/login", json=credentials)
    body = response.json()

    assert response.status_code == 200
    assert body["email"] == user_email
    assert "id" in body


def test_login_unauthorized(client):
    """POST /auth/login. - 200"""

    credentials = {"email": user_email, "password": "invalid"}
    response = client.post("/api/auth/login", json=credentials)
    body = response.json()

    assert response.status_code == 401
    assert "detail" in body


def test_logout(client):
    """POST /auth/logout. - 200"""

    response = client.post("/api/auth/logout")

    assert response.status_code == 200
    assert "detail" in response.json()


def test_reset_password(client, get_token):
    """POST /auth/login. - 200"""

    token = get_token(user_email)
    new_password = "TestingPassword123"
    reset_json = {"token": token, "password": new_password}
    response = client.post("/api/auth/reset-password", json=reset_json)

    assert response.status_code == 200
    assert "detail" in response.json()

    credentials = {"email": user_email, "password": new_password}
    response = client.post("/api/auth/login", json=credentials)

    assert response.status_code == 200
