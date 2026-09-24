def test_register(client):
    resp = client.post(
        "/auth/register",
        json={"email": "new@example.com", "password": "secret123"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == "new@example.com"
    assert "id" in data
    assert "hashed_password" not in data
    assert "password" not in data


def test_register_duplicate(client, auth_headers):
    resp = client.post(
        "/auth/register",
        json={"email": "user@example.com", "password": "secret123"},
    )
    assert resp.status_code == 400


def test_register_invalid_email(client):
    resp = client.post(
        "/auth/register", json={"email": "not-an-email", "password": "secret123"}
    )
    assert resp.status_code == 422


def test_login_success(client, auth_headers):
    # auth_headers fixture already registered user@example.com
    resp = client.post(
        "/auth/login",
        data={"username": "user@example.com", "password": "secret123"},
    )
    assert resp.status_code == 200
    assert "access_token" in resp.json()


def test_login_wrong_password(client, auth_headers):
    resp = client.post(
        "/auth/login",
        data={"username": "user@example.com", "password": "wrongpass"},
    )
    assert resp.status_code == 401


def test_me_unauthorized(client):
    resp = client.get("/users/me")
    assert resp.status_code == 401


def test_me_authorized(client, auth_headers):
    resp = client.get("/users/me", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["email"] == "user@example.com"
