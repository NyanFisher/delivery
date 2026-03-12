import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from microarch.delivery.adapters.out.postgres.models import OrderModel
from microarch.delivery.core.domain.model.order.enums import OrderStatusEnum
from microarch.delivery.core.domain.model.order.order import Order
from microarch.delivery.core.ports.order_repository import IOrderRepository


class SqlAlchemyOrderRepository(IOrderRepository):
    def __init__(self, async_session: AsyncSession) -> None:
        self._async_session = async_session

    async def save(self, order: Order) -> None:
        order_model = OrderModel.from_entity(order)
        await self._async_session.merge(order_model)
        await self._async_session.flush()

    async def get_by_id(self, id_: uuid.UUID) -> Order | None:
        model = await self._async_session.scalar(select(OrderModel).where(OrderModel.id_ == id_))
        return model.to_entity() if model else None

    async def get_created_order(self) -> Order | None:
        model = await self._async_session.scalar(select(OrderModel).where(OrderModel.status == OrderStatusEnum.CREATED))
        return model.to_entity() if model else None

    async def get_assigned_orders(self) -> list[Order]:
        models = await self._async_session.scalars(
            select(OrderModel).where(OrderModel.status == OrderStatusEnum.ASSIGNED),
        )
        return [model.to_entity() for model in models.all()]
