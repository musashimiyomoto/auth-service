import secrets
from datetime import UTC, datetime, timedelta

from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User
from db.repositories import PermissionRepository, UserRepository
from enums import ActionEnum, ResourceEnum
from exceptions import (
    AuthCodeInvalidError,
    AuthCredentialsError,
    AuthPermissionsError,
    UserAlreadyActiveError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from settings import auth_settings
from utils.crypto import pwd_context
from utils.email import send_email
from utils.redis import get_verify_code, set_verify_code


class AuthUsecase:
    def __init__(self):
        self._user_repository = UserRepository()
        self._permission_repository = PermissionRepository()

    @staticmethod
    def _create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
        """Create an access token.

        Args:
            data: The data to encode.
            expires_delta: The expiration time.

        Returns:
            The access token.

        """
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.now(tz=UTC) + expires_delta
        else:
            expire = datetime.now(tz=UTC) + timedelta(
                minutes=auth_settings.access_token_expire_minutes
            )

        to_encode.update({"exp": expire})

        return jwt.encode(
            claims=to_encode,
            key=auth_settings.secret_key,
            algorithm=auth_settings.algorithm,
        )

    def get_payload(self, token: str) -> dict:
        """Get the payload from the token.

        Args:
            token: The token.

        Returns:
            The payload.

        Raises:
            AuthCredentialsError: If the token is invalid.

        """
        try:
            return jwt.decode(
                token=token,
                key=auth_settings.secret_key,
                algorithms=[auth_settings.algorithm],
            )
        except JWTError as e:
            raise AuthCredentialsError from e

    @staticmethod
    def _generate_code() -> str:
        """Generate a code.

        Returns:
            The code.

        """
        return str(secrets.randbelow(900000) + 100000)

    async def _authenticate(
        self, session: AsyncSession, email: str, password: str
    ) -> User:
        """Authenticate a user.

        Args:
            session: The session.
            email: The email.
            password: The password.

        Returns:
            The user.

        Raises:
            AuthCredentialsError: If the user is not authenticated.

        """
        user = await self._user_repository.get_by(session=session, email=email)

        if (
            not user
            or not user.is_active
            or not user.hashed_password
            or not pwd_context.verify(secret=password, hash=user.hashed_password)
        ):
            raise AuthCredentialsError

        return user

    async def _get_user_by_email(self, session: AsyncSession, email: str) -> User:
        """Get a user by email.

        Args:
            session: The session.
            email: The email.

        Returns:
            The user.

        Raises:
            UserNotFoundError: If the user is not found.

        """
        user = await self._user_repository.get_by(session=session, email=email)
        if not user:
            raise UserNotFoundError

        return user

    async def get_current(
        self,
        session: AsyncSession,
        token: str,
        action: ActionEnum,
        resource: ResourceEnum,
    ) -> User:
        """Get the current user and check permissions.

        Args:
            session: The session.
            token: The token.
            action: The action.
            resource: The resource.

        Returns:
            The user.

        Raises:
            AuthCredentialsError: If the token is invalid.
            AuthPermissionsError: If the user does not have permission to perform the action.

        """
        payload = self.get_payload(token=token)
        email = payload.get("sub")
        role = payload.get("role")

        if email is None or role is None:
            raise AuthCredentialsError

        user = await self._user_repository.get_by(session=session, email=email)

        if not user or not user.is_active:
            raise AuthCredentialsError

        if not await self._permission_repository.get_by(
            session=session, role=role, action=action, resource=resource
        ):
            raise AuthPermissionsError

        return user

    async def login(self, session: AsyncSession, email: str, password: str) -> str:
        """Login a user.

        Args:
            session: The session.
            email: The email.
            password: The password.

        Returns:
            The token.

        Raises:
            AuthCredentialsError: If the user is not authenticated.

        """
        user = await self._authenticate(
            session=session,
            email=email,
            password=password,
        )

        if not user:
            raise AuthCredentialsError

        return self._create_access_token(
            data={"sub": user.email, "role": user.role.value},
            expires_delta=timedelta(minutes=auth_settings.access_token_expire_minutes),
        )

    async def register(
        self,
        session: AsyncSession,
        email: str,
        password: str,
        first_name: str | None = None,
        last_name: str | None = None,
    ) -> User:
        """Register a user.

        Args:
            session: The session.
            email: The email.
            password: The password.
            first_name: The first name.
            last_name: The last name.

        Returns:
            The user.

        Raises:
            UserAlreadyExistsError: If the user already exists.

        """
        if await self._user_repository.get_by(session=session, email=email):
            raise UserAlreadyExistsError

        return await self._user_repository.create(
            session=session,
            data={
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "hashed_password": pwd_context.hash(secret=password),
                "is_active": False,
            },
        )

    async def send_email_code(self, session: AsyncSession, email: str) -> None:
        """Send an email code.

        Args:
            session: The session.
            email: The email.

        Raises:
            UserAlreadyActiveError: If the user is already active.

        """
        user = await self._get_user_by_email(session=session, email=email)

        if user.is_active:
            raise UserAlreadyActiveError

        code = self._generate_code()
        await set_verify_code(identifier=user.email, code=code)

        html_content = (
            "<html><body><p>Code, which should be copied and used for "
            "authorization:</p><h3>{code}</h3><p>This message was sent by a robot, "
            "which does not check incoming mail</p></body></html>"
        ).format(code=code)

        send_email(
            email=user.email,
            html_content=html_content,
            subject="Your verification code",
        )

    async def verify_email(self, email: str, code: str, session: AsyncSession) -> None:
        """Verify an email.

        Args:
            email: The email.
            code: The code.
            session: The session.

        Raises:
            UserAlreadyActiveError: If the user is already active.
            AuthCodeInvalidError: If the code is invalid.

        """
        user = await self._get_user_by_email(session=session, email=email)

        if user.is_active:
            raise UserAlreadyActiveError

        if await get_verify_code(identifier=user.email) != code:
            raise AuthCodeInvalidError

        await self._user_repository.update_by(
            session=session,
            data={"is_active": True},
            id=user.id,
        )
