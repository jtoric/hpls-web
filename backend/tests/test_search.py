def test_search_empty_query(client):
    response = client.get("/api/search?q=")
    data = response.json()
    assert data["posts"] == []
    assert data["pages"] == []


def test_search_short_query(client):
    response = client.get("/api/search?q=a")
    data = response.json()
    assert data["posts"] == []
    assert data["pages"] == []


def test_search_finds_posts(client, auth_headers):
    client.post("/api/posts", json={
        "title": "Državno prvenstvo 2026",
        "content": "<p>Rezultati</p>",
    }, headers=auth_headers)

    response = client.get("/api/search?q=državno")
    data = response.json()
    assert len(data["posts"]) == 1
    assert data["posts"][0]["title"] == "Državno prvenstvo 2026"


def test_search_finds_pages(client, auth_headers):
    client.post("/api/pages", json={
        "title": "Anti doping",
        "slug": "anti-doping",
        "content": "<p>Pravila</p>",
    }, headers=auth_headers)

    response = client.get("/api/search?q=doping")
    data = response.json()
    assert len(data["pages"]) == 1


def test_search_no_results(client, auth_headers):
    client.post("/api/posts", json={"title": "Test"}, headers=auth_headers)

    response = client.get("/api/search?q=nepostojece")
    data = response.json()
    assert len(data["posts"]) == 0
    assert len(data["pages"]) == 0


def test_search_excludes_unpublished(client, auth_headers):
    client.post("/api/posts", json={
        "title": "Skrivena vijest",
        "published": False,
    }, headers=auth_headers)

    response = client.get("/api/search?q=skrivena")
    assert len(response.json()["posts"]) == 0
