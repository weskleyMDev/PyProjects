from http import HTTPStatus

from fastapi.testclient import TestClient
from freezegun import freeze_time
from jwt import decode  # type: ignore

from fast_zero.models.user import User
from fast_zero.schemas.token import Token
from fast_zero.security import create_access_token
from fast_zero.settings import settings


def test_token_jwt():
    data = {"sub": "test@test.com"}
    token = create_access_token(data)

    token = decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM or "HS256"]
    )

    assert token["sub"] == data["sub"]
    assert token["exp"]


def test_invalid_token(client: TestClient):
    response = client.delete(
        "/users/1", headers={"Authorization": "Bearer invalid-token"}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Invalid token!"}


def test_expires_token(client: TestClient, user: User):
    with freeze_time("2026-10-02 10:00:00"):
        response = client.post(
            "/auth/token",
            data={"username": user.username, "password": user.clean_password},  # type: ignore
        )

        assert response.status_code == HTTPStatus.OK
        token = response.json()["access_token"]

    with freeze_time("2026-10-02 10:16:00"):
        response = client.delete(
            f"/users/{user.user_id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {"detail": "Token expired!"}


def test_refresh_token(client: TestClient, token: Token):
    response = client.post(
        "/auth/refresh-token", headers={"Authorization": f"Bearer {token}"}
    )

    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "Bearer"


def test_expires_token_cant_refresh(client: TestClient, user: User):
    with freeze_time("2026-10-02 10:00:00"):
        response = client.post(
            "/auth/token",
            data={"username": user.username, "password": user.clean_password},  # type: ignore
        )

        assert response.status_code == HTTPStatus.OK
        token = response.json()["access_token"]

    with freeze_time("2026-10-02 10:16:00"):
        response = client.post(
            "/auth/refresh-token",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {"detail": "Token expired!"}
