import typing
from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from microarch.delivery.application_properties import ApplicationSettings
from microarch.delivery.core.domain.services.order_dispatcher import IOrderDispatcher, OrderDispatcher
from microarch.delivery.core.domain.uow import DeliveryUnitOfWork


async def provide_properties() -> ApplicationSettings:
    return ApplicationSettings()


async def provide_order_dispatcher() -> IOrderDispatcher:
    return OrderDispatcher()


async def provide_async_session_factory(
    properties: typing.Annotated[ApplicationSettings, Depends(provide_properties)],
) -> AsyncGenerator[async_sessionmaker[AsyncSession]]:
    engine = create_async_engine(url=properties.db_properties.dsn)
    yield async_sessionmaker(bind=engine, autoflush=False, autocommit=False)
    await engine.dispose()


async def provide_uow(
    async_session_factory: typing.Annotated[async_sessionmaker[AsyncSession], Depends(provide_async_session_factory)],
) -> DeliveryUnitOfWork:
    return DeliveryUnitOfWork(async_session_factory=async_session_factory)
