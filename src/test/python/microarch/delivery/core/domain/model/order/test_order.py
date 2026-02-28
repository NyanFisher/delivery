import uuid

from libs.errs.guard import Guard
from microarch.delivery.core.domain.model.courier import Courier
from microarch.delivery.core.domain.model.kernel.location import Location
from microarch.delivery.core.domain.model.order import Order, OrderStatusEnum

BASKET_ID = uuid.uuid4()
LOCATION = Location.create(1, 1).value
COURIER = Courier.create(name="Олег", speed=2, location=LOCATION).value


class TestOrder:
    def assert_order(
        self,
        order: Order,
        expected_location: Location,
        expected_volume: int,
        expected_status: OrderStatusEnum,
        expected_courier_id: uuid.UUID | None = None,
    ) -> None:
        assert order.id_ is not None
        assert order.location == expected_location
        assert order.volume == expected_volume
        assert order.status == expected_status
        assert order.courier_id == expected_courier_id

    def test_success_create(self) -> None:
        result = Order.create(BASKET_ID, LOCATION, volume=10)

        assert result.is_success
        self.assert_order(result.value, LOCATION, 10, OrderStatusEnum.CREATED)

    def test_failure_create_if_empty_order_id(self) -> None:
        result = Order.create(Guard.EMPTY_UUID, LOCATION, volume=10)

        assert result.is_failure
        assert result.error.code == "value.is.required"

    def test_failure_create_if_volume_less_than_min_volume(self) -> None:
        result = Order.create(BASKET_ID, LOCATION, volume=0)

        assert result.is_failure
        assert result.error.code == "value.must.be.greater.or.equal"

    def test_success_assign(self) -> None:
        order = Order.create(BASKET_ID, LOCATION, volume=10).value

        result = order.assign(COURIER)

        assert result.is_success
        self.assert_order(order, LOCATION, 10, OrderStatusEnum.ASSIGNED, COURIER.id_)

    def test_failure_assign(self) -> None:
        order = Order.create(BASKET_ID, LOCATION, volume=10).value
        order.assign(COURIER)

        result = order.assign(COURIER)

        assert result.is_failure
        assert result.error.code == "status.is.not.created"

    def test_success_complete(self) -> None:
        order = Order.create(BASKET_ID, LOCATION, volume=10).value
        order.assign(COURIER)

        result = order.complete()

        assert result.is_success
        self.assert_order(order, LOCATION, 10, OrderStatusEnum.COMPLETED, COURIER.id_)

    def test_failure_complete(self) -> None:
        order = Order.create(BASKET_ID, LOCATION, volume=10).value

        result = order.complete()

        assert result.is_failure
        assert result.error.code == "status.is.not.assigned"
