def signup(client, email="sam@example.com", password="hunter22!!"):
    return client.post("/auth/register", json={"email": email, "password": password})


def test_register_returns_token(client):
    r = signup(client)
    assert r.status_code == 201
    assert r.json()["access_token"]


def test_duplicate_email_rejected(client):
    signup(client)
    assert signup(client, email="SAM@example.com").status_code == 409


def test_short_password_rejected(client):
    assert signup(client, password="short").status_code == 422


def test_login_wrong_password(client):
    signup(client)
    r = client.post("/auth/login", json={"email": "sam@example.com", "password": "nope-nope-nope"})
    assert r.status_code == 401


def test_login_ok(client):
    signup(client)
    r = client.post("/auth/login", json={"email": "sam@example.com", "password": "hunter22!!"})
    assert r.status_code == 200


def test_protected_route_needs_token(client):
    assert client.get("/documents").status_code == 401


def test_protected_route_rejects_garbage_token(client):
    r = client.get("/documents", headers={"Authorization": "Bearer abc.def.ghi"})
    assert r.status_code == 401
