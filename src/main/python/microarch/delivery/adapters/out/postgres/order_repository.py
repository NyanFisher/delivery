from sqlalchemy.ext.asyncio import AsyncSession

from microarch.delivery.adapters.out.postgres.models import OrderModel
from microarch.delivery.core.domain.model.order.order import Order
from microarch.delivery.core.ports.order_repository import IOrderrepository


class SqlAlchemyOrderRepository(IOrderrepository):
    def __init__(self, async_session: AsyncSession) -> None:
        self._async_session = async_session

    async def add(self, order: Order) -> None:
        order_model = OrderModel.from_entity(order)

        self._async_session.add(order_model)

        await self._async_session.flush()
