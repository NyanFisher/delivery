import typing
import uuid

from libs.ddd.aggregate import Aggregate
from libs.errs import Error, GeneralErrors, Guard, Result, UnitResult

from microarch.delivery.core.domain.model.courier.storage_place import StoragePlace
from microarch.delivery.core.domain.model.kernel.location import Location
from microarch.delivery.core.domain.model.kernel.speed import Speed
from microarch.delivery.core.domain.model.kernel.volume import Volume

if typing.TYPE_CHECKING:
    from microarch.delivery.core.domain.model.order import Order


class Courier(Aggregate[uuid.UUID]):
    def __init__(
        self,
        name: str,
        speed: Speed,
        location: Location,
        id_: uuid.UUID | None = None,
        storage_places: list[StoragePlace] | None = None,
    ) -> None:
        # Do not call the constructor directly. Use the `create` method to create.
        super().__init__(id_ or uuid.uuid4())
        self._name = name
        self._speed = speed
        self._location = location
        self._storage_places = storage_places or []

    @property
    def name(self) -> str:
        return self._name

    @property
    def speed(self) -> Speed:
        return self._speed

    @property
    def location(self) -> Location:
        return self._location

    @property
    def storage_places(self) -> list[StoragePlace]:
        return self._storage_places

    @classmethod
    def create(cls, name: str, speed: Speed, location: Location) -> Result[typing.Self, Error]:
        if err := Guard.against_null_or_empty(name, "name"):
            return Result.failure(err)

        cls_ = cls(name, speed, location)

        result_volume = Volume.create(10)
        if result_volume.is_failure:
            return Result.failure(result_volume.error)

        result = cls_.add_storage_place("backpack", result_volume.value)
        if result.is_failure:
            return Result.failure(result.error)

        return Result.success(cls_)

    def add_storage_place(self, name: str, volume: Volume) -> UnitResult[Error]:
        result = StoragePlace.create(name, volume)

        if result.is_failure:
            return UnitResult.failure(result.error)

        self._storage_places.append(result.value)

        return UnitResult.success()

    def can_take_order(self, order: "Order") -> bool:
        return bool(self._get_empty_storage_place(order))

    def take_order(self, order: "Order") -> UnitResult[Error]:
        if not self.can_take_order(order):
            return UnitResult.failure(Error("no.free.storage.place", "No free storage place"))

        empty_sp = typing.cast("StoragePlace", self._get_empty_storage_place(order))

        result = empty_sp.store(typing.cast("uuid.UUID", order.id_), order.volume)
        if result.is_failure:
            return UnitResult.failure(result.error)

        return UnitResult.success()

    def complete_order(self, order: "Order") -> UnitResult[Error]:
        sp = next((sp for sp in self._storage_places if sp.order_id == order.id_), None)
        if sp is None:
            return UnitResult.failure(GeneralErrors.not_found("order", order.id_))

        result = sp.clear(typing.cast("uuid.UUID", order.id_))
        if result.is_failure:
            return UnitResult.failure(result.error)

        return UnitResult.success()

    def calculate_time_to_location(self, location: Location) -> float:
        return self._location.distance_to(location) / self._speed.value

    def move(self, target: Location) -> UnitResult[Error]:
        dif_x = target.x - self._location.x
        dif_y = target.y - self._location.y
        cruising_range = self._speed.value

        move_x = max(-cruising_range, min(dif_x, cruising_range))
        cruising_range -= abs(move_x)

        move_y = max(-cruising_range, min(dif_y, cruising_range))
        location_create_result = Location.create(
            x=self._location.x + move_x,
            y=self._location.y + move_y,
        )

        if location_create_result.is_failure:
            return UnitResult.failure(location_create_result.error)

        self._location = location_create_result.value
        return UnitResult.success()

    def _get_empty_storage_place(self, order: "Order") -> StoragePlace | None:
        return next((sp for sp in self._storage_places if sp.can_store(order.volume)), None)
