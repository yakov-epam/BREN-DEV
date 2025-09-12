async def test_health_check(http_client):
    r = await http_client.get("/health", timeout=3)
    assert r.status_code == 200
    assert r.json().get("status") == "ok"
    print("Health check")
