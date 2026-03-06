import typing
import uuid

from libs.ddd.aggregate import Aggregate
from libs.errs import Error, Guard, Result, UnitResult

from microarch.delivery.core.domain.model.kernel.location import Location
from microarch.delivery.core.domain.model.kernel.volume import Volume
from microarch.delivery.core.domain.model.order.enums import OrderStatusEnum

if typing.TYPE_CHECKING:
    from microarch.delivery.core.domain.model.courier import Courier


class Order(Aggregate[uuid.UUID]):
    def __init__(self, order_id: uuid.UUID, location: Location, volume: Volume) -> None:
        # Do not call the constructor directly. Use the `create` method to create.
        super().__init__(order_id)
        self._location = location
        self._volume = volume
        self._status: OrderStatusEnum | None = None
        self._courier_id: uuid.UUID | None = None

    @property
    def location(self) -> Location:
        return self._location

    @property
    def volume(self) -> Volume:
        return self._volume

    @property
    def status(self) -> OrderStatusEnum:
        return typing.cast("OrderStatusEnum", self._status)

    @property
    def courier_id(self) -> uuid.UUID | None:
        return self._courier_id

    @classmethod
    def create(cls, order_id: uuid.UUID, location: Location, volume: Volume) -> Result[typing.Self, Error]:
        if err := Guard.against_null_or_empty_uuid(order_id, "order_id"):
            return Result.failure(err)

        cls_ = cls(order_id, location, volume)
        cls_._status = OrderStatusEnum.CREATED

        return Result.success(cls_)

    def assign(self, courier: "Courier") -> UnitResult[Error]:
        if self._status != OrderStatusEnum.CREATED:
            return UnitResult.failure(Error("status.is.not.created", "It is impossible to assign the order"))

        self._courier_id = courier.id_
        self._status = OrderStatusEnum.ASSIGNED
        return UnitResult.success()

    def complete(self) -> UnitResult[Error]:
        if self._status != OrderStatusEnum.ASSIGNED:
            return UnitResult.failure(Error("status.is.not.assigned", "It is impossible to complete the order"))

        self._status = OrderStatusEnum.COMPLETED
        return UnitResult.success()
