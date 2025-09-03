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


class TestUserMeUpdate(BaseTestCase):
    url = "/user/me"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        await PermissionFactory.create_async(
            session=self.session,
            role=RoleEnum.USER,
            action=ActionEnum.UPDATE,
            resource=ResourceEnum.USER,
        )
        user, headers = await self.create_user_and_get_token()
        update_data = {"first_name": "Updated John", "last_name": "Updated Doe"}

        response = await self.client.patch(
            url=self.url, json=update_data, headers=headers
        )

        data = await self.assert_response_ok(response=response)
        assert data["id"] == user["id"]
        assert data["email"] == user["email"]
        assert data["first_name"] == update_data["first_name"]
        assert data["last_name"] == update_data["last_name"]


class TestUserMeDelete(BaseTestCase):
    url = "/user/me"

    @pytest.mark.asyncio
    async def test_ok(self) -> None:
        await PermissionFactory.create_async(
            session=self.session,
            role=RoleEnum.USER,
            action=ActionEnum.DELETE,
            resource=ResourceEnum.USER,
        )
        _, headers = await self.create_user_and_get_token()

        response = await self.client.delete(url=self.url, headers=headers)

        await self.assert_response_no_content(response=response)
