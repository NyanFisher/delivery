import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from microarch.delivery.adapters.out.postgres.models import CourierModel, StoragePlaceModel
from microarch.delivery.core.domain.model.courier.courier import Courier
from microarch.delivery.core.ports.courier_repository import ICourierRepository


class SqlAlchemyCourierRepository(ICourierRepository):
    def __init__(self, async_session: AsyncSession) -> None:
        self._async_session = async_session

    async def save(self, courier: Courier) -> None:
        courier_model = CourierModel.from_entity(courier)
        await self._async_session.merge(courier_model)
        await self._async_session.flush()

    async def get_by_id(self, id_: uuid.UUID) -> Courier | None:
        courier_model = await self._async_session.scalar(select(CourierModel).where(CourierModel.id_ == id_))

        return courier_model.to_entity() if courier_model else None

    async def get_free_couriers(self) -> list[Courier]:
        query = select(CourierModel).where(~CourierModel.storage_places.any(StoragePlaceModel.order_id.isnot(None)))

        models = await self._async_session.scalars(query)

        return [model.to_entity() for model in models.all()]
