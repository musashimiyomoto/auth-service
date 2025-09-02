from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import Base
from enums import RoleEnum


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, unique=True, comment="ID"
    )

    first_name: Mapped[str | None] = mapped_column(comment="First name")
    last_name: Mapped[str | None] = mapped_column(comment="Last name")
    email: Mapped[str] = mapped_column(index=True, comment="Email")
    role: Mapped[RoleEnum] = mapped_column(comment="Role")

    hashed_password: Mapped[str | None] = mapped_column(comment="Hashed password")

    is_active: Mapped[bool] = mapped_column(default=True, comment="Is active")

    last_login: Mapped[datetime | None] = mapped_column(comment="Last login")

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), comment="Created at"
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now(), comment="Updated at"
    )
