import uuid

from libs.errs import Guard
from microarch.delivery.core.domain.model.courier import Courier
from microarch.delivery.core.domain.model.kernel.location import Location
from microarch.delivery.core.domain.model.kernel.speed import Speed
from microarch.delivery.core.domain.model.kernel.volume import Volume
from microarch.delivery.core.domain.model.order import Order, OrderStatusEnum

from python.helpers import create_volume

BASKET_ID = uuid.uuid4()
LOCATION = Location.create(1, 1).value
VOLUME = create_volume(10)
SPEED = Speed.create(2).value
NAME = "Олег"
COURIER = Courier.create(name=NAME, speed=SPEED, location=LOCATION).value


class TestOrder:
    def assert_order(
        self,
        order: Order,
        expected_location: Location = LOCATION,
        expected_volume: Volume = VOLUME,
        expected_status: OrderStatusEnum = OrderStatusEnum.CREATED,
        expected_courier_id: uuid.UUID | None = None,
    ) -> None:
        assert order.id_ is not None
        assert order.location == expected_location
        assert order.volume == expected_volume
        assert order.status == expected_status
        assert order.courier_id == expected_courier_id

    def test_success_create(self) -> None:
        result = Order.create(BASKET_ID, LOCATION, VOLUME)

        assert result.is_success
        self.assert_order(result.value)

    def test_failure_create_if_empty_order_id(self) -> None:
        result = Order.create(Guard.EMPTY_UUID, LOCATION, VOLUME)

        assert result.is_failure
        assert result.error.code == "value.is.required"

    def test_success_assign(self) -> None:
        order = Order.create(BASKET_ID, LOCATION, VOLUME).value

        result = order.assign(COURIER)

        assert result.is_success
        self.assert_order(order, expected_status=OrderStatusEnum.ASSIGNED, expected_courier_id=COURIER.id_)

    def test_failure_assign(self) -> None:
        order = Order.create(BASKET_ID, LOCATION, VOLUME).value
        order.assign(COURIER)

        result = order.assign(COURIER)

        assert result.is_failure
        assert result.error.code == "status.is.not.created"

    def test_success_complete(self) -> None:
        order = Order.create(BASKET_ID, LOCATION, VOLUME).value
        order.assign(COURIER)

        result = order.complete()

        assert result.is_success
        self.assert_order(order, expected_status=OrderStatusEnum.COMPLETED, expected_courier_id=COURIER.id_)

    def test_failure_complete(self) -> None:
        order = Order.create(BASKET_ID, LOCATION, VOLUME).value

        result = order.complete()

        assert result.is_failure
        assert result.error.code == "status.is.not.assigned"
