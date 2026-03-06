import typing
from collections.abc import Iterable

from libs.errs import Error, Result

from microarch.delivery.core.domain.model.courier import Courier
from microarch.delivery.core.domain.model.order import Order
from microarch.delivery.core.domain.model.order.enums import OrderStatusEnum


class IOrderDispatcher(typing.Protocol):
    def dispatch(self, order: Order, couriers: Iterable[Courier]) -> Result[Courier, Error]: ...


class OrderDispatcher(IOrderDispatcher):
    _order_is_not_created = Error("order.is.not.created", "Order is not 'created' status")
    _list_courier_is_empty = Error("list.of.courier.is.empty", "List of courier is empty")
    _there_are_no_suitable_couriers = Error("there.are.no.suitable.couriers", "There are no suitable couriers.")

    def dispatch(self, order: Order, couriers: Iterable[Courier]) -> Result[Courier, Error]:
        if order.status is not OrderStatusEnum.CREATED:
            return Result.failure(self._order_is_not_created)
        if not couriers:
            return Result.failure(self._list_courier_is_empty)

        time_to_courier = {c.calculate_time_to_location(order.location): c for c in couriers if c.can_take_order(order)}

        if not time_to_courier:
            return Result.failure(self._there_are_no_suitable_couriers)

        fast_courier = time_to_courier[min(time_to_courier.keys())]

        result = order.assign(courier=fast_courier)
        if result.is_failure:
            return Result.failure(result.error)

        result = fast_courier.take_order(order)
        if result.is_failure:
            return Result.failure(result.error)

        return Result.success(fast_courier)
