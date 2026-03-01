import typing
import uuid

from libs.ddd.base_entity import BaseEntity
from libs.errs import Error, Result
from libs.errs.guard import Guard
from libs.errs.unit_result import UnitResult


class StoragePlace(BaseEntity[uuid.UUID]):
    MIN_TOTAL_VOLUME: typing.Final = 1

    def __init__(
        self,
        name: str,
        total_volume: int,
    ) -> None:
        super().__init__(uuid.uuid4())
        self._name = name
        self._total_volume = total_volume
        self._order_id: uuid.UUID | None = None

    @property
    def name(self) -> str:
        return self._name

    @property
    def total_volume(self) -> int:
        return self._total_volume

    @property
    def order_id(self) -> uuid.UUID | None:
        return self._order_id

    @classmethod
    def create(cls, name: str, total_volume: int) -> Result[typing.Self, Error]:
        if err := Guard.against_null_or_empty(name, "name"):
            return Result.failure(err)
        if err := Guard.against_less_than(total_volume, cls.MIN_TOTAL_VOLUME, "total_volume"):
            return Result.failure(err)

        return Result.success(cls(name=name, total_volume=total_volume))

    @property
    def is_occupied(self) -> bool:
        return self._order_id is not None

    def can_store(self, volume: int) -> bool:
        return self._order_id is None and volume <= self._total_volume

    def store(self, order_id: uuid.UUID, volume: int) -> UnitResult[Error]:
        if self._order_id is not None:
            err = Error("already.contains.another.order", "The storage location already contains another order")
            return UnitResult.failure(err)
        if err := Guard.against_null_or_empty_uuid(order_id, "order_id"):  # type: ignore[assignment]
            return UnitResult.failure(err)
        if err := Guard.against_out_of_range(volume, self.MIN_TOTAL_VOLUME, self._total_volume, "volume"):  # type: ignore[assignment]
            return UnitResult.failure(err)

        self._order_id = order_id
        return UnitResult.success()

    def clear(self, order_id: uuid.UUID) -> UnitResult[Error]:
        if err := Guard.against_null_or_empty_uuid(order_id, "order_id"):
            return UnitResult.failure(err)

        if self._order_id is None or self._order_id != order_id:
            err = Error("order.id.does.not.match", "The order ID does not match the one stored in the storage place")
            return UnitResult.failure(err)

        self._order_id = None
        return UnitResult.success()
