from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(80), nullable=False, unique=True
    )
    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    def __repr__(self):  # pragma: no cover
        return (
            f"User(id:{self.user_id}, username:{self.username!r}, "
            f"email:{self.email!r})"
        )
