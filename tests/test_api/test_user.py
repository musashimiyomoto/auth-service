import pytest

from enums import ActionEnum, ResourceEnum, RoleEnum
from tests.factories import PermissionFactory
from tests.test_api.base import BaseTestCase


class TestUserMe(BaseTestCase):
    url = "/user/me"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        await PermissionFactory.create_async(
            session=self.session,
            role=RoleEnum.USER,
            action=ActionEnum.READ,
            resource=ResourceEnum.USER,
        )
        user, headers = await self.create_user_and_get_token()

        response = await self.client.get(url=self.url, headers=headers)

        data = await self.assert_response_ok(response=response)
        assert data["id"] == user["id"]
        assert data["email"] == user["email"]
