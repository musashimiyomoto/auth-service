from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User
from db.repositories import UserRepository


class UserUsecase:
    def __init__(self):
        self._user_repository = UserRepository()

    async def update_by(
        self, session: AsyncSession, data: dict[str, Any], id: int
    ) -> User:
        """Update a user by id.

        Args:
            session: The session.
            data: The data.
            id: The id.

        Returns:
            The user.

        """
        return await self._user_repository.update_by(session=session, data=data, id=id)

    async def delete_by(self, session: AsyncSession, id: int) -> None:
        """Delete a user by id.

        Args:
            session: The session.
            id: The id.

        """
        await self._user_repository.update_by(
            session=session, data={"is_active": False}, id=id
        )
