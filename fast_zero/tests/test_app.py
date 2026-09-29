from http import HTTPStatus
from typing import Any

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from fast_zero.models.user import User
from fast_zero.schemas.user import UserDTO


def test_create_user_return_created(
    client: TestClient, input_data: dict[str, Any], output_data: dict[str, Any]
):
    response = client.post(
        "/users/",
        json=input_data,
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == output_data


def test_create_user_return_conflict_username(client: TestClient, user: User):
    user_schema = {
        "username": user.username,
        "password": user.password,
        "email": "other@mail.com",
    }
    response = client.post("/users/", json=user_schema)
    assert response.status_code == HTTPStatus.CONFLICT


def test_create_user_return_conflict_email(client: TestClient, user: User):
    user_schema = {
        "username": "other_username",
        "password": user.password,
        "email": user.email,
    }
    response = client.post("/users/", json=user_schema)
    assert response.status_code == HTTPStatus.CONFLICT


def test_get_users_return_ok(client: TestClient, user: User):
    user_schema = UserDTO.model_validate(user).model_dump()
    response = client.get("/users/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": [user_schema]}


def test_update_user_return_ok(
    client: TestClient, user: User, session: Session
):
    user_schema = {
        "username": "new_username",
        "password": "new_password",
        "email": "new@email.com",
    }
    response = client.put(f"/users/{user.user_id}", json=user_schema)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "user_id": user.user_id,
        "username": user_schema["username"],
        "email": user_schema["email"],
    }

    updated_user = session.get(User, user.user_id)

    assert updated_user is not None
    assert updated_user.username == user_schema["username"]
    assert updated_user.password == user_schema["password"]
    assert updated_user.email == user_schema["email"]


def test_update_user_raise_not_found(client: TestClient):
    user_schema = {
        "username": "new_username",
        "password": "new_password",
        "email": "new@email.com",
    }
    response = client.put("/users/-1", json=user_schema)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_remove_user_return_no_content(client: TestClient, user: User):
    response = client.delete(f"users/{user.user_id}")
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_remove_user_raise_not_found(client: TestClient):
    response = client.delete("/users/-1")
    assert response.status_code == HTTPStatus.NOT_FOUND
