import typing
from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from microarch.delivery.adapters.out.postgres.courier_repository import SqlAlchemyCourierRepository
from microarch.delivery.adapters.out.postgres.order_repository import SqlAlchemyOrderRepository
from microarch.delivery.core.ports.courier_repository import ICourierRepository
from microarch.delivery.core.ports.order_repository import IOrderRepository


class DeliveryUnitOfWork:
    orders: IOrderRepository
    couriers: ICourierRepository
    session: AsyncSession

    def __init__(self, async_session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._async_session_factory = async_session_factory

    async def __aenter__(self) -> typing.Self:
        self.session = self._async_session_factory()
        self.orders = SqlAlchemyOrderRepository(self.session)
        self.couriers = SqlAlchemyCourierRepository(self.session)
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.session.rollback()
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()
