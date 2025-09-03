import pytest

from enums import ActionEnum, ResourceEnum, RoleEnum
from tests.factories import PermissionFactory
from tests.test_api.base import BaseTestCase


class TestPermissionList(BaseTestCase):
    url = "/permission/list"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        await PermissionFactory.create_async(
            session=self.session,
            role=RoleEnum.USER,
            action=ActionEnum.READ,
            resource=ResourceEnum.PERMISSION,
        )

        _, headers = await self.create_user_and_get_token()

        response = await self.client.get(url=self.url, headers=headers)

        data = await self.assert_response_ok(response=response)
        assert isinstance(data, list)
        assert len(data) == 1


class TestPermissionUpdate(BaseTestCase):
    url = "/permission"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        await PermissionFactory.create_async(
            session=self.session,
            role=RoleEnum.USER,
            action=ActionEnum.UPDATE,
            resource=ResourceEnum.PERMISSION,
        )
        _, headers = await self.create_user_and_get_token()

        response = await self.client.patch(
            url=self.url,
            params={
                "role": RoleEnum.USER.value,
                "action": ActionEnum.UPDATE.value,
                "resource": ResourceEnum.PERMISSION.value,
            },
            json={"is_active": False},
            headers=headers,
        )

        data = await self.assert_response_ok(response=response)
        assert data["role"] == RoleEnum.USER.value
        assert data["action"] == ActionEnum.UPDATE.value
        assert data["resource"] == ResourceEnum.PERMISSION.value
        assert data["is_active"] is False
