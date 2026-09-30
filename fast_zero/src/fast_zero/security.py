from typing import Any
from zoneinfo import ZoneInfo

from pwdlib import PasswordHash
from jwt import encode # type: ignore
from secrets import token_hex
from datetime import datetime, timedelta

SECRET_KEY = token_hex(128)
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 15

pwd_context = PasswordHash.recommended()


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict[str, Any]):
    to_encode = data.copy()

    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({'exp': expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt