from http import HTTPStatus
from typing import Any

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from fast_zero.models.user import User
from fast_zero.schemas.user import UserDTO
from fast_zero.security import verify_password


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


def test_get_users_return_ok(client: TestClient, user: User, token: str):
    user_schema = UserDTO.model_validate(user).model_dump()
    response = client.get(
        "/users/", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": [user_schema]}


def test_update_user_return_ok(
    client: TestClient, user: User, session: Session, token: str
):
    user_schema = {
        "username": "new_username",
        "password": "new_password",
        "email": "new@email.com",
    }
    response = client.put(
        f"/users/{user.user_id}",
        json=user_schema,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "user_id": user.user_id,
        "username": user_schema["username"],
        "email": user_schema["email"],
    }

    updated_user = session.get(User, user.user_id)

    assert updated_user is not None
    assert updated_user.username == user_schema["username"]
    assert updated_user.email == user_schema["email"]

    assert verify_password(user_schema["password"], updated_user.password)


def test_update_user_raise_not_found(client: TestClient, token: str):
    user_schema = {
        "username": "new_username",
        "password": "new_password",
        "email": "new@email.com",
    }
    response = client.put(
        "/users/-1",
        json=user_schema,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_user_return_forbidden(
    client: TestClient, other_user: User, token: str
):
    user_schema = {
        "username": "new_username",
        "password": "new_password",
        "email": "new@email.com",
    }
    response = client.put(
        f"/users/{other_user.user_id}",
        json=user_schema,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {"detail": "Not enough permission!"}


def test_remove_user_return_no_content(
    client: TestClient, user: User, token: str
):
    response = client.delete(
        f"users/{user.user_id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_remove_user_raise_not_found(client: TestClient, token: str):
    response = client.delete(
        "/users/-1", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User with id=-1 not found!"}


def test_remove_user_raise_forbidden(
    client: TestClient, other_user: User, token: str
):
    response = client.delete(
        f"/users/{other_user.user_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {"detail": "Not enough permission!"}


def test_get_token(client: TestClient, user: User):
    response = client.post(
        "/auth/token",
        data={"username": user.username, "password": user.clean_password},  # type: ignore
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token["token_type"] == "Bearer"
    assert "access_token" in token
