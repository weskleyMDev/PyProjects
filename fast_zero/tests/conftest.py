import pytest
from factory.base import Factory
from factory.declarations import LazyAttribute, Sequence
from fastapi.testclient import TestClient
from sqlalchemy import Engine
from sqlalchemy.orm import Session

from fast_zero.app import app
from fast_zero.database import get_session, test_engine
from fast_zero.models.base import Base
from fast_zero.models.user import User
from fast_zero.security import get_password_hash


class UserFactory(Factory):  # type: ignore
    class Meta:  # type: ignore
        model = User

    username = Sequence(lambda n: f"test{n}")  # type: ignore
    password = LazyAttribute(lambda obj: f"{obj.username}drop")  # type: ignore
    email = LazyAttribute(lambda obj: f"{obj.username}@mail.com")  # type: ignore


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
    pwd = "user_password"
    user = UserFactory(
        password=get_password_hash(pwd),
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = pwd  # type: ignore

    return user


@pytest.fixture
def other_user(session: Session):
    pwd = "user_password"
    user = UserFactory(
        password=get_password_hash(pwd),
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
        "username": "user_username",
        "password": "user_password",
        "email": "user_username@mail.com",
    }


@pytest.fixture
def output_data() -> dict[str, object]:
    return {
        "user_id": 1,
        "username": "user_username",
        "email": "user_username@mail.com",
    }
