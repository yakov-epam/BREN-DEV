import pytest
import random

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
async def test_get_book_by_id(role, expected_status, client):
    r = await client.get("/books/1")
    assert r.status_code == expected_status
    if r.status_code == 200:
        book = r.json()
        assert book["id"] == 1 and book["title"] == "To Kill a Mockingbird"


@pytest.mark.parametrize(
    "role,expected_status,client",
    (
        (enums.UserRole.ADMIN, 200, enums.UserRole.ADMIN),
        (enums.UserRole.USER, 200, enums.UserRole.USER),
        (None, 401, None),
    ),
    indirect=["client"],
)
async def test_get_book_by_title(role, expected_status, client):
    r = await client.get("/books", params={"title": "1984"})
    assert r.status_code == expected_status
    if r.status_code == 200:
        assert any(b["title"] == "1984" for b in r.json()["items"])


@pytest.mark.parametrize(
    "role,expected_status,client",
    (
        (enums.UserRole.ADMIN, 201, enums.UserRole.ADMIN),
        (enums.UserRole.USER, 403, enums.UserRole.USER),
        (None, 401, None),
    ),
    indirect=["client"],
)
async def test_add_book(role, expected_status, client):
    new_id = random.randint(1000, 9999)
    payload = {
        "id": new_id,
        "title": "The Hobbit",
        "author": "J. R. R. Tolkien",
        "pages": 310,
        "rating": 4.9,
        "price": 15.99,
    }
    r = await client.post("/books", json=payload)
    assert r.status_code == expected_status
    if r.status_code == 201:
        r = await client.get(f"/books/{new_id}")
        assert r.status_code == 200 and r.json()["title"] == "The Hobbit"


@pytest.mark.parametrize(
    "role,expected_status,client",
    (
        (enums.UserRole.ADMIN, 200, enums.UserRole.ADMIN),
        (enums.UserRole.USER, 403, enums.UserRole.USER),
        (None, 401, None),
    ),
    indirect=["client"],
)
async def test_update_price_and_rating(role, expected_status, client, create_book):
    patch = {"price": 12.49, "rating": 4.8}
    r = await client.put(f"/books/{create_book.id}", json=patch)
    assert r.status_code == expected_status
    if r.status_code == 200:
        data = r.json()
        assert data["price"] == patch["price"] and data["rating"] == patch["rating"]


@pytest.mark.parametrize(
    "role,expected_status,client",
    (
        (enums.UserRole.ADMIN, 200, enums.UserRole.ADMIN),
        (enums.UserRole.USER, 200, enums.UserRole.USER),
        (None, 401, None),
    ),
    indirect=["client"],
)
async def test_filter_by_pages(role, expected_status, client):
    r = await client.get("/books", params={"pages_gt": 299})
    assert r.status_code == expected_status
    books = r.json()
    if r.status_code == 200:
        assert books and all(b["pages"] >= 300 for b in books["items"])


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
    r = await client.post("/books", json=bad_payload)
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
async def test_validation_invalid_values(role, expected_status, client):
    bad_payload = {
        "id": -5,
        "title": "Bad Data",
        "author": "Nobody",
        "pages": "three hundred",
        "rating": 6.0,
        "price": -1.00,
    }
    r = await client.post("/books", json=bad_payload)
    assert r.status_code == expected_status, "Server accepted invalid value types/ranges"
