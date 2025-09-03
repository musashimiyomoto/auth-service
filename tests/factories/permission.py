from db.models.permission import Permission
from enums import ActionEnum, ResourceEnum, RoleEnum
from tests.factories.base import AsyncSQLAlchemyModelFactory


class PermissionFactory(AsyncSQLAlchemyModelFactory):
    class Meta:  # type: ignore
        model = Permission

    role = RoleEnum.USER
    action = ActionEnum.READ
    resource = ResourceEnum.USER

    is_active = True
