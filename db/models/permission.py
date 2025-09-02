from datetime import datetime

from sqlalchemy import func, Index
from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import Base
from enums import RoleEnum, ActionEnum, ResourceEnum


class Permission(Base):
    __tablename__ = "permissions"
    __table_args__ = (
        Index(name="index_role_action_resource", "role", "action", "resource"),
    )

    role: Mapped[RoleEnum] = mapped_column(primary_key=True, comment="Role")
    action: Mapped[ActionEnum] = mapped_column(primary_key=True, comment="Action")
    resource: Mapped[ResourceEnum] = mapped_column(primary_key=True, comment="Resource")

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), comment="Created at"
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now(), comment="Updated at"
    )
