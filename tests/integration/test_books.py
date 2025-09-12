import random


async def test_get_book_by_id(http_client):
    r = await http_client.get("/books/1")
    assert r.status_code == 200
    book = r.json()
    assert book["id"] == 1 and book["title"] == "To Kill a Mockingbird"


async def test_get_book_by_title(http_client):
    r = await http_client.get("/books", params={"title": "1984"})
    assert r.status_code == 200
    assert any(b["title"] == "1984" for b in r.json()["items"])


async def test_add_book(http_client):
    new_id = random.randint(1000, 9999)
    payload = {
        "id": new_id,
        "title": "The Hobbit",
        "author": "J. R. R. Tolkien",
        "pages": 310,
        "rating": 4.9,
        "price": 15.99,
    }
    r = await http_client.post("/books", json=payload)
    assert r.status_code in (200, 201)
    r = await http_client.get(f"/books/{new_id}")
    assert r.status_code == 200 and r.json()["title"] == "The Hobbit"
    return new_id


async def test_update_price_and_rating(create_book, http_client):
    patch = {"price": 12.49, "rating": 4.8}
    r = await http_client.put(f"/books/{create_book.id}", json=patch)
    assert r.status_code == 200
    data = r.json()
    assert data["price"] == patch["price"] and data["rating"] == patch["rating"]


async def test_filter_by_pages(http_client):
    r = await http_client.get("/books", params={"pages_gt": 299})
    assert r.status_code == 200
    books = r.json()
    assert books and all(b["pages"] >= 300 for b in books["items"])


async def test_validation_missing_fields(http_client):
    bad_payload = {"title": "Missing many fields"}
    r = await http_client.post("/books", json=bad_payload)
    assert r.status_code in (400, 422), "Server did not reject missing-field payload"


async def test_validation_invalid_values(http_client):
    bad_payload = {
        "id": -5,
        "title": "Bad Data",
        "author": "Nobody",
        "pages": "three hundred",
        "rating": 6.0,
        "price": -1.00,
    }
    r = await http_client.post("/books", json=bad_payload)
    assert r.status_code in (400, 422), "Server accepted invalid value types/ranges"
