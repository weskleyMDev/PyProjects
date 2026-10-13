from pydantic import BaseModel, ConfigDict

from fast_zero.models.todo import TodoState


class TodoSchema(BaseModel):
    title: str
    description: str
    state: TodoState


class TodoDto(TodoSchema):
    model_config = ConfigDict(from_attributes=True)

    todo_id: int


class TodoList(BaseModel):
    todos: list[TodoDto]
