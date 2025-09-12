import pytest

from db import enums


@pytest.mark.parametrize(
    "role,expected_status,client",
    (
        (enums.UserRole.ADMIN, 200, enums.UserRole.ADMIN),
        (enums.UserRole.USER, 200, enums.UserRole.USER),
        (None, 401, None),
    ),
    indirect=["client"],
)
async def test_get_user_by_id(role, expected_status, client):
    r = await client.get("/users/1")
    assert r.status_code == expected_status
    if r.status_code == 200:
        user = r.json()
        assert user["id"] == 1


@pytest.mark.parametrize(
    "role,expected_status,client",
    (
        (enums.UserRole.ADMIN, 200, enums.UserRole.ADMIN),
        (enums.UserRole.USER, 200, enums.UserRole.USER),
        (None, 401, None),
    ),
    indirect=["client"],
)
async def test_get_user_by_username(role, expected_status, client):
    r = await client.get("/users", params={"username": "user"})
    assert r.status_code == expected_status
    if r.status_code == 200:
        assert any(b["username"] == "user" for b in r.json()["items"])


@pytest.mark.parametrize(
    "role,expected_status,client",
    (
        (enums.UserRole.ADMIN, 201, enums.UserRole.ADMIN),
        (enums.UserRole.USER, 403, enums.UserRole.USER),
        (None, 401, None),
    ),
    indirect=["client"],
)
async def test_add_user(role, expected_status, client):
    payload = {
        "username": f"TEST_{role}",
        "password": "testtest",
    }
    r = await client.post("/users", json=payload)
    assert r.status_code == expected_status
    if r.status_code == 201:
        r = await client.get(f"/users/{r.json()['id']}")
        assert r.status_code == 200 and r.json()["username"] == f"TEST_{role}"


@pytest.mark.parametrize(
    "role,expected_status,client",
    (
        (enums.UserRole.ADMIN, 200, enums.UserRole.ADMIN),
        (enums.UserRole.USER, 403, enums.UserRole.USER),
        (None, 401, None),
    ),
    indirect=["client"],
)
async def test_update_user(role, expected_status, client, create_user_user):
    patch = {"username": "new_test"}
    r = await client.put(f"/users/{create_user_user.id}", json=patch)
    assert r.status_code == expected_status
    if r.status_code == 200:
        data = r.json()
        assert data["username"] == patch["username"]


@pytest.mark.parametrize(
    "role,expected_status,client",
    (
        (enums.UserRole.ADMIN, 422, enums.UserRole.ADMIN),
        (enums.UserRole.USER, 403, enums.UserRole.USER),
        (None, 401, None),
    ),
    indirect=["client"],
)
async def test_validation_missing_fields(role, expected_status, client):
    bad_payload = {"title": "Missing many fields"}
    r = await client.post("/users", json=bad_payload)
    assert r.status_code == expected_status, "Server did not reject missing-field payload"


@pytest.mark.parametrize(
    "role,expected_status,client",
    (
        (enums.UserRole.ADMIN, 422, enums.UserRole.ADMIN),
        (enums.UserRole.USER, 403, enums.UserRole.USER),
        (None, 401, None),
    ),
    indirect=["client"],
)
async def test_validation_invalid_username(role, expected_status, client):
    bad_payload = {
        "username": "Bad Data",
        "password": "testtest",
    }
    r = await client.post("/users", json=bad_payload)
    assert r.status_code == expected_status, "Server accepted invalid value types/ranges"


@pytest.mark.parametrize(
    "role,expected_status,client",
    (
        (enums.UserRole.ADMIN, 422, enums.UserRole.ADMIN),
        (enums.UserRole.USER, 403, enums.UserRole.USER),
        (None, 401, None),
    ),
    indirect=["client"],
)
async def test_validation_invalid_password(role, expected_status, client):
    bad_payload = {
        "username": "ok_here",
        "password": "t",
    }
    r = await client.post("/users", json=bad_payload)
    assert r.status_code == expected_status, "Server accepted invalid value types/ranges"
