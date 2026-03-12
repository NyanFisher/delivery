from collections.abc import Generator
from typing import AsyncGenerator
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from testcontainers.postgres import PostgresContainer

import pytest

from microarch.delivery.adapters.out.postgres.models import BaseModel


@pytest.fixture(scope="session", autouse=True)
def postgres_container() -> Generator[PostgresContainer]:
    with PostgresContainer("postgres:16", driver="psycopg") as postgres:
        engine = create_engine(postgres.get_connection_url())
        with engine.begin() as conn:
            BaseModel.metadata.drop_all(conn)
            BaseModel.metadata.create_all(conn)
        yield postgres
        engine.dispose()

@pytest.fixture
async def async_session(postgres_container: PostgresContainer) -> AsyncGenerator[AsyncSession]:
    engine = create_async_engine(postgres_container.get_connection_url())

    async with AsyncSession(engine) as session:
        yield session
        await session.rollback()

    await engine.dispose()
