import typing
import uuid

import pytest
from microarch.delivery.adapters.out.postgres.courier_repository import SqlAlchemyCourierRepository
from microarch.delivery.adapters.out.postgres.models import OrderModel
from microarch.delivery.adapters.out.postgres.order_repository import SqlAlchemyOrderRepository
from microarch.delivery.core.domain.model.order.enums import OrderStatusEnum
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from python.constants import BASKET_ID, COURIER_LOCATION, COURIER_NAME, COURIER_SPEED, ORDER_LOCATION, ORDER_VOLUME
from python.helpers import create_courier, create_order


@pytest.fixture
def sut(async_session: AsyncSession) -> SqlAlchemyOrderRepository:
    return SqlAlchemyOrderRepository(async_session)


class TestSqlalchemyOrderRepository:
    async def test_save_new_entity(self, sut: SqlAlchemyOrderRepository, async_session: AsyncSession) -> None:
        order = create_order(BASKET_ID, ORDER_LOCATION, ORDER_VOLUME)

        await sut.save(order)

        result = await async_session.scalar(select(OrderModel).where(OrderModel.id_ == order.id_))
        assert result is not None
        assert result.to_entity() == order

    async def test_save_update_entity(self, sut: SqlAlchemyOrderRepository, async_session: AsyncSession) -> None:
        # Arrange
        order = create_order(BASKET_ID, ORDER_LOCATION, ORDER_VOLUME)
        await sut.save(order)

        courier = create_courier(COURIER_NAME, COURIER_SPEED, COURIER_LOCATION)
        courier_repository = SqlAlchemyCourierRepository(async_session)
        await courier_repository.save(courier)

        order.assign(courier)

        # Act
        await sut.save(order)

        result = await async_session.scalar(select(OrderModel).where(OrderModel.id_ == order.id_))
        assert result is not None
        assert result.to_entity() == order
        assert result.status == OrderStatusEnum.ASSIGNED

    async def test_get_none_by_id(self, sut: SqlAlchemyOrderRepository) -> None:
        assert await sut.get_by_id(uuid.uuid4()) is None

    async def test_get_by_id(self, sut: SqlAlchemyOrderRepository) -> None:
        order = create_order(BASKET_ID, ORDER_LOCATION, ORDER_VOLUME)
        await sut.save(order)

        result = await sut.get_by_id(typing.cast("uuid.UUID", order.id_))

        assert result == order

    async def test_get_none_if_not_found_created(self, sut: SqlAlchemyOrderRepository) -> None:
        assert await sut.get_created_order() is None

    async def test_get_created_order(self, sut: SqlAlchemyOrderRepository) -> None:
        order = create_order(BASKET_ID, ORDER_LOCATION, ORDER_VOLUME)
        await sut.save(order)

        result = await sut.get_created_order()

        assert result == order

    async def test_dont_get_assigned_orders(self, sut: SqlAlchemyOrderRepository) -> None:
        assert await sut.get_assigned_orders() == []

    async def test_get_assigned_orders(self, sut: SqlAlchemyOrderRepository, async_session: AsyncSession) -> None:
        # Arrange
        order = create_order(BASKET_ID, ORDER_LOCATION, ORDER_VOLUME)
        await sut.save(order)

        courier = create_courier(COURIER_NAME, COURIER_SPEED, COURIER_LOCATION)
        courier_repository = SqlAlchemyCourierRepository(async_session)
        await courier_repository.save(courier)

        order.assign(courier)
        await sut.save(order)

        # Act
        result = await sut.get_assigned_orders()

        # Assert
        assert result == [order]
