from http import HTTPStatus

from fastapi.testclient import TestClient
from jwt import decode  # type: ignore

from fast_zero.security import ALGORITHM, SECRET_KEY, create_access_token


def test_token_jwt():
    data = {"sub": "test@test.com"}
    token = create_access_token(data)

    token = decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert token["sub"] == data["sub"]
    assert token["exp"]


def test_invalid_token(client: TestClient):
    response = client.delete(
        "/users/1", headers={"Authorization": "Bearer invalid-token"}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Invalid credentials!"}
