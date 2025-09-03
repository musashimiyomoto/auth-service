from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from constants import ROLE_PERMISSIONS
from db.models import Permission
from db.repositories import PermissionRepository
from db.sessions import async_session


class PermissionUsecase:
    def __init__(self):
        self._permission_repository = PermissionRepository()

    async def init_permissions(self) -> list[Permission]:
        """Initialize permissions.

        Args:
            session: The session.

        Returns:
            The list of permissions.

        """
        async with async_session() as session:
            permissions = await self._permission_repository.get_all(session=session)

            if permissions != []:
                return permissions

            return await self._permission_repository.create_many(
                session=session,
                data=[
                    {
                        "role": role,
                        "action": action,
                        "resource": resource,
                        "is_active": True,
                    }
                    for role, resources in ROLE_PERMISSIONS.items()
                    for resource, actions in resources.items()
                    for action in actions
                ],
            )

    async def get_permissions(
        self, session: AsyncSession, **filters
    ) -> list[Permission]:
        """Get permissions.

        Args:
            session: The session.
            **filters: The filters.

        Returns:
            The list of permissions.

        """
        return await self._permission_repository.get_all(session=session, **filters)

    async def update_by(
        self, session: AsyncSession, data: dict[str, Any], **filters
    ) -> Permission:
        """Update permission by filters.

        Args:
            session: The session.
            data: The data.
            **filters: The filters.

        Returns:
            The permission.

        """
        return await self._permission_repository.update_by(
            session=session, data=data, **filters
        )
