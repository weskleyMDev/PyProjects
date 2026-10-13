from http import HTTPStatus

from fastapi.testclient import TestClient


def test_create_todo_return_ok(client: TestClient, token: str):
    response = client.post(
        "/todos/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "test todo",
            "description": "testing todo",
            "state": "draft",
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "todo_id": 1,
        "title": "test todo",
        "description": "testing todo",
        "state": "draft",
    }
