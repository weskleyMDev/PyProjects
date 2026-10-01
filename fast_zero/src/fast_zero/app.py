from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models.user import User
from fast_zero.schemas.token import Token
from fast_zero.schemas.user import UserBase, UserDTO, UserList
from fast_zero.security import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)

app = FastAPI()


@app.get("/users/", response_model=UserList)
def get_users(
    limit: int = 10,
    skip: int = 0,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
) -> UserList:
    db_users = session.scalars(select(User).limit(limit).offset(skip)).all()
    return UserList.model_validate({"users": db_users})


@app.post("/users/", status_code=HTTPStatus.CREATED, response_model=UserDTO)
def create_user(
    user: UserBase, session: Session = Depends(get_session)
) -> UserDTO:
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )
    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=f"User: {user.username} already exists!",
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail=f"Email: {user.email} already exists!",
            )
    data = user.model_dump()
    data["password"] = get_password_hash(data["password"])
    db_user = User(**data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return UserDTO.model_validate(db_user)


@app.put("/users/{user_id}", response_model=UserDTO)
def update_user(
    user_id: int,
    user: UserBase,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> UserDTO:
    updated_user = session.scalar(select(User).where(User.user_id == user_id))
    if not updated_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"User with id={user_id} not found!",
        )
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail="Not enough permission!"
        )

    current_user.username = user.username
    current_user.password = get_password_hash(user.password)
    current_user.email = user.email

    session.commit()
    session.refresh(current_user)

    return UserDTO.model_validate(current_user)


@app.delete("/users/{user_id}", status_code=HTTPStatus.NO_CONTENT)
def remove_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> None:
    user = session.scalar(select(User).where(User.user_id == user_id))
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"User with id={user_id} not found!",
        )
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail="Not enough permission!"
        )

    session.delete(current_user)
    session.commit()


@app.post("/token", response_model=Token)
def get_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = session.scalar(
        select(User).where(User.username == form_data.username)
    )

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Incorrect email or password!",
        )

    access_token = create_access_token(data={"sub": user.username})

    return {"access_token": access_token, "token_type": "Bearer"}
