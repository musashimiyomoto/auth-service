from typing import Annotated

from fastapi import APIRouter, Body, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import auth, db, permission
from api.schemas import (
    PermissionFilterSchema,
    PermissionResponseSchema,
    PermissionStatusUpdateSchema,
    UserResponseSchema,
)
from enums import ActionEnum, ResourceEnum
from usecases import PermissionUsecase

router = APIRouter(prefix="/permission", tags=["Permission"])


@router.get(path="/list")
async def get_permissions(
    filters: Annotated[
        PermissionFilterSchema, Query(description="Filters for get permissions")
    ],
    usecase: Annotated[
        PermissionUsecase, Depends(dependency=permission.get_permission_usecase)
    ],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    current_user: Annotated[
        UserResponseSchema,
        Depends(
            dependency=auth.get_current_user(
                action=ActionEnum.READ, resource=ResourceEnum.PERMISSION
            )
        ),
    ],
) -> list[PermissionResponseSchema]:
    return [
        PermissionResponseSchema.model_validate(permission)
        for permission in await usecase.get_permissions(
            session=session, **filters.model_dump(exclude_none=True)
        )
    ]


@router.patch(path="")
async def update_permission(
    data: Annotated[
        PermissionStatusUpdateSchema,
        Body(description="Data for update permission status"),
    ],
    filters: Annotated[
        PermissionFilterSchema,
        Query(description="Filters for update permission status"),
    ],
    usecase: Annotated[
        PermissionUsecase, Depends(dependency=permission.get_permission_usecase)
    ],
    session: Annotated[AsyncSession, Depends(dependency=db.get_session)],
    current_user: Annotated[
        UserResponseSchema,
        Depends(
            dependency=auth.get_current_user(
                action=ActionEnum.UPDATE, resource=ResourceEnum.PERMISSION
            )
        ),
    ],
) -> PermissionResponseSchema:
    return PermissionResponseSchema.model_validate(
        await usecase.update_by(
            session=session,
            data=data.model_dump(),
            **filters.model_dump(exclude_none=True),
        )
    )
