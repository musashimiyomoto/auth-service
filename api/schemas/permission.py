from datetime import datetime

from pydantic import BaseModel, Field

from enums import ActionEnum, ResourceEnum, RoleEnum


class PermissionBaseSchema(BaseModel):
    role: RoleEnum = Field(default=..., description="Role")
    action: ActionEnum = Field(default=..., description="Action")
    resource: ResourceEnum = Field(default=..., description="Resource")
    is_active: bool = Field(default=..., description="Is active")


class PermissionFilterSchema(BaseModel):
    role: RoleEnum | None = Field(default=None, description="Role")
    action: ActionEnum | None = Field(default=None, description="Action")
    resource: ResourceEnum | None = Field(default=None, description="Resource")


class PermissionStatusUpdateSchema(BaseModel):
    is_active: bool = Field(default=..., description="Is active")


class PermissionResponseSchema(PermissionBaseSchema):
    created_at: datetime = Field(default=..., description="Created at")
    updated_at: datetime = Field(default=..., description="Updated at")

    class Config:
        from_attributes = True
