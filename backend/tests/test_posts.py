import pytest


def test_create_post(client, auth_headers):
    response = client.post("/api/posts", json={
        "title": "Testna vijest",
        "content": "<p>Sadržaj vijesti</p>",
        "excerpt": "Kratki opis",
        "category": "news",
    }, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Testna vijest"
    assert data["slug"] == "testna-vijest"
    assert data["category"] == "news"
    assert data["published"] is True


def test_create_post_unauthenticated(client):
    response = client.post("/api/posts", json={
        "title": "Test",
        "content": "test",
    })
    assert response.status_code == 401


def test_create_post_duplicate_slug(client, auth_headers):
    client.post("/api/posts", json={"title": "Duplikat"}, headers=auth_headers)
    response = client.post("/api/posts", json={"title": "Duplikat"}, headers=auth_headers)
    assert response.status_code == 201
    assert response.json()["slug"] == "duplikat-1"


def test_list_posts_empty(client):
    response = client.get("/api/posts")
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0


def test_list_posts_with_data(client, auth_headers):
    client.post("/api/posts", json={"title": "Vijest 1", "category": "news"}, headers=auth_headers)
    client.post("/api/posts", json={"title": "Vijest 2", "category": "news"}, headers=auth_headers)
    client.post("/api/posts", json={"title": "Kalendar 1", "category": "calendar"}, headers=auth_headers)

    # All posts
    response = client.get("/api/posts")
    assert response.json()["total"] == 3

    # Filter by category
    response = client.get("/api/posts?category=news")
    assert response.json()["total"] == 2

    response = client.get("/api/posts?category=calendar")
    assert response.json()["total"] == 1


def test_list_posts_pagination(client, auth_headers):
    for i in range(5):
        client.post("/api/posts", json={"title": f"Post {i}"}, headers=auth_headers)

    response = client.get("/api/posts?limit=2&page=1")
    data = response.json()
    assert len(data["items"]) == 2
    assert data["total"] == 5
    assert data["pages"] == 3


def test_get_post_by_slug(client, auth_headers):
    client.post("/api/posts", json={
        "title": "Moja vijest",
        "content": "<p>Detalji</p>",
    }, headers=auth_headers)

    response = client.get("/api/posts/moja-vijest")
    assert response.status_code == 200
    assert response.json()["title"] == "Moja vijest"


def test_get_post_not_found(client):
    response = client.get("/api/posts/ne-postoji")
    assert response.status_code == 404


def test_update_post(client, auth_headers):
    create = client.post("/api/posts", json={"title": "Original"}, headers=auth_headers)
    post_id = create.json()["id"]

    response = client.put(f"/api/posts/{post_id}", json={
        "title": "Ažurirano",
        "content": "<p>Novo</p>",
    }, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Ažurirano"


def test_update_post_unauthenticated(client, auth_headers):
    create = client.post("/api/posts", json={"title": "Test"}, headers=auth_headers)
    post_id = create.json()["id"]

    response = client.put(f"/api/posts/{post_id}", json={"title": "Hack"})
    assert response.status_code == 401


def test_delete_post(client, auth_headers):
    create = client.post("/api/posts", json={"title": "Za brisanje"}, headers=auth_headers)
    post_id = create.json()["id"]

    response = client.delete(f"/api/posts/{post_id}", headers=auth_headers)
    assert response.status_code == 204

    response = client.get("/api/posts/za-brisanje")
    assert response.status_code == 404


def test_delete_post_not_found(client, auth_headers):
    response = client.delete("/api/posts/999", headers=auth_headers)
    assert response.status_code == 404


def test_unpublished_post_not_in_public_list(client, auth_headers):
    client.post("/api/posts", json={
        "title": "Skrivena",
        "published": False,
    }, headers=auth_headers)

    response = client.get("/api/posts")
    assert response.json()["total"] == 0

    # But visible in admin list
    response = client.get("/api/posts/admin/all", headers=auth_headers)
    assert response.json()["total"] == 1
