from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from fast_zero.dependencies import T_CurrentUser, T_Session
from fast_zero.models.todo import Todo, TodoState
from fast_zero.schemas.todo import TodoDto, TodoList, TodoSchema

router = APIRouter(prefix="/todos", tags=["todos"])


@router.post("/", response_model=TodoDto, status_code=HTTPStatus.CREATED)
def create_todo(
    todo: TodoSchema, user: T_CurrentUser, session: T_Session
) -> TodoDto:
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=user.user_id,
    )

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return TodoDto.model_validate(db_todo)


@router.get("/", response_model=TodoList)
def get_todos(
    user: T_CurrentUser,
    session: T_Session,
    title: str | None = None,
    description: str | None = None,
    state: TodoState | None = None,
    offset: int | None = None,
    limit: int | None = None,
):
    query = select(Todo).where(Todo.user_id == user.user_id)

    if title:
        query = query.filter(Todo.title.contains(title))

    if description:
        query = query.filter(Todo.description.contains(description))

    if state:
        query = query.filter(Todo.state == state)

    todos = session.scalars(query.offset(offset).limit(limit)).all()

    return TodoList.model_validate({"todos": todos})


@router.delete("/{todo_id}", status_code=HTTPStatus.NO_CONTENT)
def remove_todo(todo_id: int, user: T_CurrentUser, session: T_Session):
    todo = session.scalar(
        select(Todo).where(
            Todo.user_id == user.user_id, Todo.todo_id == todo_id
        )
    )

    if not todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"TODO with id={todo_id} not found!",
        )

    session.delete(todo)
    session.commit()
