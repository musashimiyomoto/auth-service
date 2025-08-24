import factory
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

fake = Faker("en_US")


class AsyncSQLAlchemyModelFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:  # type: ignore
        abstract = True
        sqlalchemy_session_persistence = "commit"

    @classmethod
    async def create_async(cls, session: AsyncSession, **kwargs):
        instance = cls.build(**kwargs)
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return instance

    @classmethod
    async def create_batch_async(cls, session: AsyncSession, size: int, **kwargs):
        instances = []
        for _ in range(size):
            instance = cls.build(**kwargs)
            session.add(instance)
            instances.append(instance)

        await session.commit()

        for instance in instances:
            await session.refresh(instance)

        return instances
