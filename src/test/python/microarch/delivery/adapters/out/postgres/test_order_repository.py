from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from microarch.delivery.adapters.out.postgres.models import OrderModel
from microarch.delivery.adapters.out.postgres.order_repository import SqlAlchemyOrderRepository
from microarch.delivery.core.domain.model.order.order import Order
from python.constants import BASKET_ID, ORDER_LOCATION, ORDER_VOLUME
from python.helpers import create_order


class TestSqlalchemyOrderRepository:
    async def test_add(self, async_session: AsyncSession) -> None:
        order = create_order(BASKET_ID, ORDER_LOCATION, ORDER_VOLUME)
        sut = SqlAlchemyOrderRepository(async_session)

        await sut.add(order)

        result = await async_session.scalar(select(OrderModel).where(OrderModel.id_ == order.id_))
        assert result is not None
        assert result.to_entity() == order

