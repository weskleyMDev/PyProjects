import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine
from sqlalchemy.orm import Session

from fast_zero.app import app
from fast_zero.database import get_session, test_engine
from fast_zero.models.base import Base
from fast_zero.models.user import User
from fast_zero.security import get_password_hash


@pytest.fixture
def client(session: Session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client
    app.dependency_overrides.clear()


@pytest.fixture(scope="session")
def engine():
    engine = test_engine
    return engine


@pytest.fixture
def session(engine: Engine):
    Base.metadata.create_all(test_engine)
    with Session(engine) as session:
        yield session
    Base.metadata.drop_all(test_engine)


@pytest.fixture
def user(session: Session):
    pwd = "your_password"
    user = User(
        username="your_username",
        password=get_password_hash(pwd),
        email="your_username@mail.com",
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = pwd  # type: ignore

    return user


@pytest.fixture
def token(client: TestClient, user: User):
    response = client.post(
        "/auth/token",
        data={"username": user.username, "password": user.clean_password},  # type: ignore
    )
    return response.json()["access_token"]


@pytest.fixture
def input_data() -> dict[str, str]:
    return {
        "username": "your_username",
        "password": "your_password",
        "email": "your_username@mail.com",
    }


@pytest.fixture
def output_data() -> dict[str, object]:
    return {
        "user_id": 1,
        "username": "your_username",
        "email": "your_username@mail.com",
    }
