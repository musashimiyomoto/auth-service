from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from enums import RoleEnum


class UserBaseSchema(BaseModel):
    first_name: str | None = Field(default=None, description="First name")
    last_name: str | None = Field(default=None, description="Last name")
    email: EmailStr = Field(default=..., description="Email of the user")


class UserCreateSchema(UserBaseSchema):
    password: str = Field(default=..., description="Password of the user")


class UserUpdateSchema(BaseModel):
    first_name: str | None = Field(default=None, description="First name")
    last_name: str | None = Field(default=None, description="Last name")


class UserResponseSchema(UserBaseSchema):
    id: int = Field(default=..., description="ID of the user", gt=0)

    role: RoleEnum = Field(default=..., description="Role of the user")

    is_active: bool = Field(default=..., description="Is the user active")

    last_login: datetime | None = Field(default=None, description="Last login")

    created_at: datetime = Field(default=..., description="Created at")
    updated_at: datetime = Field(default=..., description="Updated at")

    class Config:
        from_attributes = True
