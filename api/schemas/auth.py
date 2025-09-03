from pydantic import BaseModel, EmailStr, Field


class LoginSchema(BaseModel):
    email: EmailStr | None = Field(default=None, description="Email of the user")
    password: str = Field(default=..., description="Password of the user")


class TokenSchema(BaseModel):
    access_token: str = Field(default=..., description="Access token")
    token_type: str = Field(default=..., description="Token type")
