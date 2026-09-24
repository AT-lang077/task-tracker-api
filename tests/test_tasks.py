from tests.conftest import register_and_login


def test_create_task_unauthorized(client):
    resp = client.post("/tasks/", json={"title": "No auth"})
    assert resp.status_code == 401


def test_task_crud_flow(client, auth_headers):
    # Create
    resp = client.post(
        "/tasks/",
        json={"title": "My task", "description": "Do it"},
        headers=auth_headers,
    )
    assert resp.status_code == 201
    task = resp.json()
    task_id = task["id"]
    assert task["title"] == "My task"
    assert task["status"] == "todo"

    # List
    resp = client.get("/tasks/", headers=auth_headers)
    assert resp.status_code == 200
    assert len(resp.json()) == 1

    # Get by id
    resp = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["id"] == task_id

    # Update
    resp = client.put(
        f"/tasks/{task_id}",
        json={"status": "done", "title": "My task updated"},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "done"

    # Delete
    resp = client.delete(f"/tasks/{task_id}", headers=auth_headers)
    assert resp.status_code == 204

    # Gone
    resp = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert resp.status_code == 404


def test_filter_by_status(client, auth_headers):
    client.post("/tasks/", json={"title": "t1", "status": "todo"}, headers=auth_headers)
    client.post("/tasks/", json={"title": "t2", "status": "done"}, headers=auth_headers)

    resp = client.get("/tasks/?status=done", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["status"] == "done"


def test_other_user_cannot_access_task(client):
    headers1 = register_and_login(client, "a@example.com", "secret123")
    headers2 = register_and_login(client, "b@example.com", "secret123")

    resp = client.post("/tasks/", json={"title": "private"}, headers=headers1)
    task_id = resp.json()["id"]

    # second user should get 404 (no access to foreign task)
    resp = client.get(f"/tasks/{task_id}", headers=headers2)
    assert resp.status_code == 404

    resp = client.get("/tasks/", headers=headers2)
    assert resp.json() == []
