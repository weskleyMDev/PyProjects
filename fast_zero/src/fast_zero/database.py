from sqlalchemy import URL, create_engine
from sqlalchemy.orm import Session

from .settings import Settings

__all__ = ["database_url", "app_engine", "test_engine"]


def _create_database_url(settings: Settings, *, is_test: bool = False):
    return URL.create(
        drivername="postgresql+psycopg",
        username=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT,
        database=settings.DATABASE_NAME
        if not is_test
        else settings.TEST_DATABASE_NAME,
    )


def _create_app_engine(settings: Settings):
    url = _create_database_url(settings)

    return create_engine(url)


def _create_test_engine(settings: Settings):
    url = _create_database_url(settings, is_test=True)

    return create_engine(url)


def get_session():  # pragma: no cover
    with Session(app_engine) as session:
        yield session


_settings = Settings()
database_url = _create_database_url(_settings)
app_engine = _create_app_engine(_settings)
test_engine = _create_test_engine(_settings)
