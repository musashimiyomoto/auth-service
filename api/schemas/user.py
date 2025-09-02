from datetime import datetime

from pydantic import BaseModel, Field

from enums import RoleEnum


class UserBaseSchema(BaseModel):
    first_name: str | None = Field(default=None, description="First name")
    last_name: str | None = Field(default=None, description="Last name")
    email: str = Field(default=..., description="Email of the user")
    role: RoleEnum = Field(default=..., description="Role of the user")


class UserCreateSchema(UserBaseSchema):
    password: str = Field(default=..., description="Password of the user")


class UserResponseSchema(UserBaseSchema):
    id: int = Field(default=..., description="ID of the user", gt=0)

    is_active: bool = Field(default=..., description="Is the user active")

    last_login: datetime | None = Field(default=None, description="Last login")

    created_at: datetime = Field(default=..., description="Created at")
    updated_at: datetime = Field(default=..., description="Updated at")

    class Config:
        from_attributes = True
