import typing
import uuid

from libs.ddd.aggregate import Aggregate
from libs.errs import Error, Result
from libs.errs.error import GeneralErrors
from libs.errs.guard import Guard
from libs.errs.unit_result import UnitResult

from microarch.delivery.core.domain.model.courier.storage_place import StoragePlace
from microarch.delivery.core.domain.model.kernel.location import Location

if typing.TYPE_CHECKING:
    from microarch.delivery.core.domain.model.order import Order


class Courier(Aggregate[uuid.UUID]):
    MIN_SPEED: typing.Final = 1

    def __init__(self, name: str, speed: int, location: Location) -> None:
        super().__init__(uuid.uuid4())
        self.name = name
        self.speed = speed
        self.location = location
        self.storage_places: list[StoragePlace] = []

    @classmethod
    def create(cls, name: str, speed: int, location: Location) -> Result[typing.Self, Error]:
        if err := Guard.against_null_or_empty(name, "name"):
            return Result.failure(err)
        if err := Guard.against_less_than(speed, cls.MIN_SPEED, "speed"):
            return Result.failure(err)

        cls_ = cls(name, speed, location)

        result = cls_.add_storage_place("backpack", 10)
        if result.is_failure:
            return Result.failure(result.error)

        return Result.success(cls_)

    def add_storage_place(self, name: str, volume: int) -> UnitResult[Error]:
        result = StoragePlace.create(name, volume)

        if result.is_failure:
            return UnitResult.failure(result.error)

        self.storage_places.append(result.value)

        return UnitResult.success()

    def can_take_order(self, order: "Order") -> bool:
        return any(sp.can_store(order.volume) for sp in self.storage_places)

    def take_order(self, order: "Order") -> UnitResult[Error]:
        empty_sp = next((sp for sp in self.storage_places if sp.can_store(order.volume)), None)
        if empty_sp is None:
            return UnitResult.failure(Error("no.free.storage.place", "No free storage place"))

        result = empty_sp.store(typing.cast("uuid.UUID", order.id_), order.volume)
        if result.is_failure:
            return UnitResult.failure(result.error)

        return UnitResult.success()

    def complete_order(self, order: "Order") -> UnitResult[Error]:
        sp = next((sp for sp in self.storage_places if sp.order_id == order.id_), None)
        if sp is None:
            return UnitResult.failure(GeneralErrors.not_found("order", order.id_))

        result = sp.clear(typing.cast("uuid.UUID", order.id_))
        if result.is_failure:
            return UnitResult.failure(result.error)

        return UnitResult.success()

    def calculate_time_to_location(self, location: Location) -> float:
        return self.location.distance_to(location) / self.speed

    def move(self, target: Location) -> UnitResult[Error]:
        dif_x = target.x - self.location.x
        dif_y = target.y - self.location.y
        cruising_range = self.speed

        move_x = max(-cruising_range, min(dif_x, cruising_range))
        cruising_range -= abs(move_x)

        move_y = max(-cruising_range, min(dif_y, cruising_range))
        location_create_result = Location.create(
            x=self.location.x + move_x,
            y=self.location.y + move_y,
        )

        if location_create_result.is_failure:
            return UnitResult.failure(location_create_result.error)

        self.location = location_create_result.value
        return UnitResult.success()
