import typing
import uuid

import pytest
from microarch.delivery.adapters.out.postgres.courier_repository import SqlAlchemyCourierRepository
from microarch.delivery.adapters.out.postgres.models import CourierModel, StoragePlaceModel
from microarch.delivery.adapters.out.postgres.order_repository import SqlAlchemyOrderRepository
from microarch.delivery.core.domain.services.order_dispatcher import OrderDispatcher
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from python.constants import BASKET_ID, COURIER_LOCATION, COURIER_NAME, COURIER_SPEED, ORDER_LOCATION, ORDER_VOLUME
from python.helpers import create_courier, create_order, create_volume


@pytest.fixture
def sut(async_session: AsyncSession) -> SqlAlchemyCourierRepository:
    return SqlAlchemyCourierRepository(async_session)


class TestSqlAlchemyCourierRepository:
    async def test_save_new_entity(
        self,
        sut: SqlAlchemyCourierRepository,
        async_session: AsyncSession,
    ) -> None:
        courier = create_courier(COURIER_NAME, COURIER_SPEED, COURIER_LOCATION)

        await sut.save(courier)

        courier_model = await async_session.scalar(select(CourierModel).where(CourierModel.id_ == courier.id_))
        assert courier_model is not None
        assert courier_model.to_entity() == courier
        sp_model = await async_session.scalar(
            select(StoragePlaceModel).where(StoragePlaceModel.id_ == courier.storage_places[0].id_),
        )
        assert sp_model is not None
        assert sp_model.to_entity() == courier.storage_places[0]

    async def test_save_update_entity(
        self,
        sut: SqlAlchemyCourierRepository,
        async_session: AsyncSession,
    ) -> None:
        courier = create_courier(COURIER_NAME, COURIER_SPEED, COURIER_LOCATION)
        await sut.save(courier)
        courier.add_storage_place("Car", create_volume(20))

        await sut.save(courier)

        courier_model = await async_session.scalar(select(CourierModel).where(CourierModel.id_ == courier.id_))
        assert courier_model is not None
        assert courier_model.to_entity() == courier
        sp_models_q = (
            select(StoragePlaceModel)
            .where(StoragePlaceModel.courier_id == courier.id_)
            .order_by(StoragePlaceModel.volume.asc())
        )
        sp_models = (await async_session.scalars(sp_models_q)).all()
        assert len(sp_models) == 2
        assert [sp_model.to_entity() for sp_model in sp_models] == courier.storage_places

    async def test_get_by_id_fetch_none(self, sut: SqlAlchemyCourierRepository) -> None:
        assert await sut.get_by_id(uuid.uuid4()) is None

    async def test_get_by_id(self, sut: SqlAlchemyCourierRepository) -> None:
        courier = create_courier(COURIER_NAME, COURIER_SPEED, COURIER_LOCATION)
        await sut.save(courier)

        result = await sut.get_by_id(typing.cast("uuid.UUID", courier.id_))
        assert result is not None
        assert result == courier

    async def test_dont_get_free_couriers_because_not_couriers(self, sut: SqlAlchemyCourierRepository) -> None:
        assert await sut.get_free_couriers() == []

    async def test_dont_get_free_couriers_because_all_couiriers_busy(
        self,
        sut: SqlAlchemyCourierRepository,
        async_session: AsyncSession,
    ) -> None:
        # Arrange
        order_repository = SqlAlchemyOrderRepository(async_session)
        order = create_order(BASKET_ID, ORDER_LOCATION, ORDER_VOLUME)
        await order_repository.save(order)

        courier = create_courier(COURIER_NAME, COURIER_SPEED, COURIER_LOCATION)
        await sut.save(courier)

        OrderDispatcher().dispatch(order, [courier])
        await order_repository.save(order)
        await sut.save(courier)

        # Act
        result = await sut.get_free_couriers()

        # Assert
        assert result == []

    async def test_get_free_couriers(
        self,
        sut: SqlAlchemyCourierRepository,
        async_session: AsyncSession,
    ) -> None:
        # Arrange
        order_repository = SqlAlchemyOrderRepository(async_session)
        order = create_order(BASKET_ID, ORDER_LOCATION, ORDER_VOLUME)
        await order_repository.save(order)

        courier = create_courier(COURIER_NAME, COURIER_SPEED, COURIER_LOCATION)
        await sut.save(courier)

        OrderDispatcher().dispatch(order, [courier])
        await order_repository.save(order)
        # Добавим в курьера свободное хранилище, но не получим его, т.к. ВСЕ хранилища должны быть free.
        courier.add_storage_place("jar", create_volume(5))
        await sut.save(courier)

        free_courier = create_courier(COURIER_NAME, COURIER_SPEED, COURIER_LOCATION)
        await sut.save(free_courier)

        # Act
        result = await sut.get_free_couriers()

        # Assert
        assert result == [free_courier]
