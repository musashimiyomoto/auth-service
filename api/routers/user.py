from typing import Annotated

from fastapi import APIRouter, Body, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import auth, db, user
from api.schemas import UserResponseSchema, UserUpdateSchema
from enums import ActionEnum, ResourceEnum

router = APIRouter(prefix="/user", tags=["User"])


@router.get(path="/me")
async def get_me(
    current_user: Annotated[
        UserResponseSchema,
        Depends(
            dependency=auth.get_current_user(
                action=ActionEnum.READ, resource=ResourceEnum.USER
            )
        ),
    ],
) -> UserResponseSchema:
    return current_user


@router.patch(path="/me")
async def update_user(
    data: Annotated[UserUpdateSchema, Body(description="Data for update user")],
    usecase: Annotated[user.UserUsecase, Depends(dependency=user.get_user_usecase)],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    current_user: Annotated[
        UserResponseSchema,
        Depends(
            dependency=auth.get_current_user(
                action=ActionEnum.UPDATE, resource=ResourceEnum.USER
            )
        ),
    ],
) -> UserResponseSchema:
    return UserResponseSchema.model_validate(
        await usecase.update_by(
            session=session, data=data.model_dump(exclude_none=True), id=current_user.id
        )
    )


@router.delete(path="/me")
async def delete_user(
    usecase: Annotated[user.UserUsecase, Depends(dependency=user.get_user_usecase)],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    current_user: Annotated[
        UserResponseSchema,
        Depends(
            dependency=auth.get_current_user(
                action=ActionEnum.DELETE, resource=ResourceEnum.USER
            )
        ),
    ],
) -> JSONResponse:
    await usecase.delete_by(session=session, id=current_user.id)
    return JSONResponse(
        content={"detail": "User deleted successfully"},
        status_code=status.HTTP_202_ACCEPTED,
    )
