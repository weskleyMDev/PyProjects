from http import HTTPStatus

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from fast_zero.models.todo import TodoState
from fast_zero.models.user import User
from tests.conftest import TodoFactory


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

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "todo_id": 1,
        "title": "test todo",
        "description": "testing todo",
        "state": "draft",
    }


def test_get_todos_should_return_five_todos(
    client: TestClient, session: Session, user: User, token: str
):
    expected_todos = 5
    session.bulk_save_objects(
        TodoFactory.create_batch(expected_todos, user_id=user.user_id)  # type: ignore
    )
    session.commit()

    response = client.get(
        "/todos/", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()["todos"]) == expected_todos


def test_get_todos_filter_title_should_return_five_todos(
    client: TestClient, session: Session, user: User, token: str
):
    expected_todos = 5
    session.bulk_save_objects(
        TodoFactory.create_batch(  # type: ignore
            expected_todos, title="text 1", user_id=user.user_id
        )
    )
    session.commit()

    response = client.get(
        "/todos/?title=text 1", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()["todos"]) == expected_todos


def test_get_todos_filter_description_should_return_five_todos(
    client: TestClient, session: Session, user: User, token: str
):
    expected_todos = 5
    session.bulk_save_objects(
        TodoFactory.create_batch(  # type: ignore
            expected_todos, description="text 1", user_id=user.user_id
        )
    )
    session.commit()

    response = client.get(
        "/todos/?description=tex",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()["todos"]) == expected_todos


def test_get_todos_filter_state_should_return_five_todos(
    client: TestClient, session: Session, user: User, token: str
):
    expected_todos = 5
    session.bulk_save_objects(
        TodoFactory.create_batch(  # type: ignore
            expected_todos, state=TodoState.draft, user_id=user.user_id
        )
    )
    session.commit()

    response = client.get(
        "/todos/?state=draft", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()["todos"]) == expected_todos


def test_delete_todo_return_no_content(
    session: Session, client: TestClient, user: User, token: str
):
    todo = TodoFactory(user_id=user.user_id)
    session.add(todo)
    session.commit()
    session.refresh(todo)

    response = client.delete(
        f"/todos/{todo.todo_id}", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.NO_CONTENT


def test_delete_todo_return_not_found(client: TestClient, token: str):
    response = client.delete(
        "/todos/10", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_todo_return_ok(
    session: Session, client: TestClient, user: User, token: str
):
    todo = TodoFactory(user_id=user.user_id)
    session.add(todo)
    session.commit()
    session.refresh(todo)

    response = client.patch(
        f"/todos/{todo.todo_id}",
        json={"title": "updated title"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()["title"] == todo.title


def test_update_todo_return_not_found(client: TestClient, token: str):
    response = client.patch(
        "/todos/10", json={}, headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
