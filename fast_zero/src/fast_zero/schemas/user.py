from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    username: str
    password: str
    email: EmailStr


class UserDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    username: str
    email: EmailStr


class UserList(BaseModel):
    users: list[UserDTO]
