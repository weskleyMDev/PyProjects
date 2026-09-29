from sqlalchemy import Engine, inspect, select
from sqlalchemy.orm import Session

from fast_zero.models.user import User


def test_user_table_exists(engine: Engine):
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    assert "users" in tables


def test_insert_user(input_data: dict[str, object], session: Session):
    user = User(**input_data)

    session.add(user)
    session.commit()

    result = session.scalar(select(User).where(User.user_id == user.user_id))

    assert result is not None
    assert result.user_id is not None
    assert result.username == user.username
    assert result.password == user.password
    assert result.email == user.email
    assert result.created_at is not None


def test_update_user(user: User, session: Session):
    user.username = "updated_username"
    session.commit()

    updated_user = session.get(User, user.user_id)

    assert updated_user is not None
    assert updated_user.username == "updated_username"


def test_remove_user(user: User, session: Session):
    user_id = user.user_id

    session.delete(user)
    session.commit()

    result = session.scalar(select(User).where(User.user_id == user_id))

    assert result is None


def test_user_repr():
    user = User(user_id=1, username="your_username", email="your@email.com")

    assert repr(user) == (
        "User(id:1, username:'your_username', email:'your@email.com')"
    )
