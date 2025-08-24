from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import db
from api.schemas import UserResponseSchema
from usecases.auth import AuthUsecase

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


async def get_current_user(
    token: Annotated[str, Depends(dependency=oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
) -> UserResponseSchema:
    """Get the current client.

    Dependencies:
        token: The token.
        session: The session.

    Returns:
        The current client.

    """
    return UserResponseSchema.model_validate(
        await AuthUsecase().get_current(token=token, session=session)
    )


def get_auth_usecase() -> AuthUsecase:
    """Get the user auth usecase.

    Returns:
        The user auth usecase.

    """
    return AuthUsecase()
