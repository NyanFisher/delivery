import typing
import uuid

from microarch.delivery.core.domain.model.courier.courier import Courier


class ICourierRepository(typing.Protocol):
    async def save(self, courier: Courier) -> None: ...
    async def get_by_id(self, id_: uuid.UUID) -> Courier | None: ...
    async def get_free_couriers(self) -> typing.Iterable[Courier]: ...
