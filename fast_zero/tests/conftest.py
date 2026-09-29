import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine
from sqlalchemy.orm import Session

from fast_zero.app import app
from fast_zero.database import get_session, test_engine
from fast_zero.models.base import Base
from fast_zero.models.user import User


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
def user(input_data: dict[str, object], session: Session):
    user = User(**input_data)

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@pytest.fixture
def input_data() -> dict[str, object]:
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
