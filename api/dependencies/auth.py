from typing import Annotated, Awaitable, Callable

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import db
from api.schemas import UserResponseSchema
from enums import ActionEnum, ResourceEnum
from usecases import AuthUsecase

security = HTTPBearer()


def get_current_user(
    action: ActionEnum, resource: ResourceEnum
) -> Callable[..., Awaitable[UserResponseSchema]]:
    """Get the user and check permissions.

    Dependencies:
        action: The action.
        resource: The resource.
        credentials: The credentials.
        session: The session.

    Returns:
        The user.

    """

    async def _dependency(
        credentials: Annotated[
            HTTPAuthorizationCredentials, Depends(dependency=security)
        ],
        session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    ) -> UserResponseSchema:
        return UserResponseSchema.model_validate(
            await AuthUsecase().get_current_user(
                token=credentials.credentials,
                session=session,
                action=action,
                resource=resource,
            )
        )

    return _dependency


def get_auth_usecase() -> AuthUsecase:
    """Get the user auth usecase.

    Returns:
        The user auth usecase.

    """
    return AuthUsecase()
