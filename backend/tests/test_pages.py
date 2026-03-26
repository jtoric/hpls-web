def test_list_pages_empty(client):
    response = client.get("/api/pages")
    assert response.status_code == 200
    assert response.json() == []


def test_create_page(client, auth_headers):
    response = client.post("/api/pages", json={
        "title": "Rekordi",
        "slug": "rekordi",
        "content": "<p>Rekordna stranica</p>",
    }, headers=auth_headers)
    assert response.status_code == 201
    assert response.json()["title"] == "Rekordi"
    assert response.json()["slug"] == "rekordi"


def test_create_page_duplicate_slug(client, auth_headers):
    client.post("/api/pages", json={"title": "A", "slug": "test"}, headers=auth_headers)
    response = client.post("/api/pages", json={"title": "B", "slug": "test"}, headers=auth_headers)
    assert response.status_code == 400


def test_create_page_unauthenticated(client):
    response = client.post("/api/pages", json={"title": "Test", "slug": "test"})
    assert response.status_code == 401


def test_get_page_by_slug(client, auth_headers):
    client.post("/api/pages", json={
        "title": "Kontakt",
        "slug": "kontakt",
        "content": "<p>Info</p>",
    }, headers=auth_headers)

    response = client.get("/api/pages/kontakt")
    assert response.status_code == 200
    assert response.json()["title"] == "Kontakt"


def test_get_page_not_found(client):
    response = client.get("/api/pages/ne-postoji")
    assert response.status_code == 404


def test_update_page(client, auth_headers):
    create = client.post("/api/pages", json={
        "title": "Original",
        "slug": "original",
    }, headers=auth_headers)
    page_id = create.json()["id"]

    response = client.put(f"/api/pages/{page_id}", json={
        "title": "Ažurirano",
        "content": "<p>Novi sadržaj</p>",
    }, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Ažurirano"
    assert response.json()["content"] == "<p>Novi sadržaj</p>"


def test_update_page_not_found(client, auth_headers):
    response = client.put("/api/pages/999", json={"title": "X"}, headers=auth_headers)
    assert response.status_code == 404


def test_pages_with_parent_slug(client, auth_headers):
    client.post("/api/pages", json={
        "title": "Pravila",
        "slug": "pravila",
        "parent_slug": "o-nama",
        "sort_order": 1,
    }, headers=auth_headers)

    response = client.get("/api/pages/pravila")
    data = response.json()
    assert data["parent_slug"] == "o-nama"
    assert data["sort_order"] == 1
