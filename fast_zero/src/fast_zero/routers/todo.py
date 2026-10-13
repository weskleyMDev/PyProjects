from http import HTTPStatus

from fastapi import APIRouter

from fast_zero.dependencies import T_CurrentUser, T_Session
from fast_zero.models.todo import Todo
from fast_zero.schemas.todo import TodoDto, TodoSchema

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
