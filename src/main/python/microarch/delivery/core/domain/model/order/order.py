import typing
import uuid

from libs.ddd.aggregate import Aggregate
from libs.errs import Error, Result
from libs.errs.guard import Guard
from libs.errs.unit_result import UnitResult

from microarch.delivery.core.domain.model.kernel.location import Location
from microarch.delivery.core.domain.model.order.enums import OrderStatusEnum

if typing.TYPE_CHECKING:
    from microarch.delivery.core.domain.model.courier import Courier


class Order(Aggregate[uuid.UUID]):
    MIN_VOLUME: typing.Final = 1

    def __init__(self, order_id: uuid.UUID, location: Location, volume: int) -> None:
        super().__init__(order_id)
        self.location = location
        self.volume = volume
        self.status: OrderStatusEnum | None = None
        self.courier_id: uuid.UUID | None = None

    @classmethod
    def create(cls, order_id: uuid.UUID, location: Location, volume: int) -> Result[typing.Self, Error]:
        if err := Guard.against_null_or_empty_uuid(order_id, "order_id"):
            return Result.failure(err)
        if err := Guard.against_less_than(volume, cls.MIN_VOLUME, "volume"):
            return Result.failure(err)

        cls_ = cls(order_id, location, volume)
        cls_.status = OrderStatusEnum.CREATED

        return Result.success(cls_)

    def assign(self, courier: "Courier") -> UnitResult[Error]:
        if self.status != OrderStatusEnum.CREATED:
            return UnitResult.failure(Error("status.is.not.created", "It is impossible to assign the order"))

        self.courier_id = courier.id_
        self.status = OrderStatusEnum.ASSIGNED
        return UnitResult.success()

    def complete(self) -> UnitResult[Error]:
        if self.status != OrderStatusEnum.ASSIGNED:
            return UnitResult.failure(Error("status.is.not.assigned", "It is impossible to complete the order"))

        self.status = OrderStatusEnum.COMPLETED
        return UnitResult.success()
