import uuid

import pytest
from microarch.delivery.core.domain.model.courier import Courier
from microarch.delivery.core.domain.model.kernel.location import Location
from microarch.delivery.core.domain.model.order.order import Order

COURIER_NAME = "Олег"
COURIER_SPEED = 2
COURIER_LOCATION = Location.create(1, 1).value

STORAGE_PLACE_UUID = uuid.uuid4()

ORDER_LOCATION = Location.create(5, 5).value
ORDER = Order.create(uuid.uuid4(), ORDER_LOCATION, 5).value


class TestCourier:
    def assert_courier(
        self,
        courier: Courier,
        expected_name: str = COURIER_NAME,
        expected_speed: int = COURIER_SPEED,
        expected_location: Location = COURIER_LOCATION,
        expected_len_storage_places: int = 1,
    ) -> None:
        assert courier.name == expected_name
        assert courier.speed == expected_speed
        assert courier.location == expected_location
        assert len(courier.storage_places) == expected_len_storage_places

    def test_success_create(self) -> None:
        result = Courier.create(name=COURIER_NAME, speed=COURIER_SPEED, location=COURIER_LOCATION)

        assert result.is_success
        self.assert_courier(result.value)

    def test_failure_create_if_name_is_empty(self) -> None:
        result = Courier.create(name="", speed=COURIER_SPEED, location=COURIER_LOCATION)

        assert result.is_failure
        assert result.error.code == "value.is.required"

    def test_failure_create_if_speed_is_less_than_min_speed(self) -> None:
        result = Courier.create(name=COURIER_NAME, speed=0, location=COURIER_LOCATION)

        assert result.is_failure
        assert result.error.code == "value.must.be.greater.or.equal"

    def test_success_add_storage_place(self) -> None:
        courier = Courier.create(name=COURIER_NAME, speed=COURIER_SPEED, location=COURIER_LOCATION).value

        result = courier.add_storage_place("new backpack", 20)

        assert result.is_success
        self.assert_courier(courier, expected_len_storage_places=2)

    def test_failure_add_storage_place(self) -> None:
        courier = Courier.create(name=COURIER_NAME, speed=COURIER_SPEED, location=COURIER_LOCATION).value

        result = courier.add_storage_place("torn backpack", 0)

        assert result.is_failure
        assert result.error.code == "value.must.be.greater.or.equal"

    def test_can_take_order(self) -> None:
        courier = Courier.create(name=COURIER_NAME, speed=COURIER_SPEED, location=COURIER_LOCATION).value

        result = courier.can_take_order(ORDER)

        assert result is True

    def test_failure_can_take_order(self) -> None:
        courier = Courier.create(name=COURIER_NAME, speed=COURIER_SPEED, location=COURIER_LOCATION).value
        biggest_order = Order.create(uuid.uuid4(), location=ORDER_LOCATION, volume=50).value

        result = courier.can_take_order(biggest_order)

        assert result is False

    def test_take_order(self) -> None:
        courier = Courier.create(name=COURIER_NAME, speed=COURIER_SPEED, location=COURIER_LOCATION).value

        result = courier.take_order(ORDER)

        assert result.is_success
        assert courier.storage_places[0].order_id == ORDER.id_

    def test_failure_take_order_if_no_free_storage_place(self) -> None:
        courier = Courier.create(name=COURIER_NAME, speed=COURIER_SPEED, location=COURIER_LOCATION).value
        courier.take_order(ORDER)

        result = courier.take_order(ORDER)

        assert result.is_failure
        assert result.error.code == "no.free.storage.place"

    def test_complete_order(self) -> None:
        courier = Courier.create(name=COURIER_NAME, speed=COURIER_SPEED, location=COURIER_LOCATION).value
        courier.take_order(ORDER)

        result = courier.complete_order(ORDER)

        assert result.is_success
        assert courier.storage_places[0].order_id is None

    def test_failure_complete_order_if_not_found_storage_by_order_id(self) -> None:
        courier = Courier.create(name=COURIER_NAME, speed=COURIER_SPEED, location=COURIER_LOCATION).value
        courier.take_order(ORDER)
        other_order = Order.create(uuid.uuid4(), location=ORDER_LOCATION, volume=10).value

        result = courier.complete_order(other_order)

        assert result.is_failure
        assert result.error.code == "record.not.found"

    @pytest.mark.parametrize(("speed", "expected"), [(1, 8), (2, 4), (4, 2)])
    def test_calculate_time_to_location(self, speed: int, expected: int) -> None:
        courier = Courier.create(name=COURIER_NAME, speed=speed, location=COURIER_LOCATION).value

        result = courier.calculate_time_to_location(ORDER_LOCATION)

        assert result == expected

    def test_move(self) -> None:
        courier = Courier.create(name=COURIER_NAME, speed=COURIER_SPEED, location=COURIER_LOCATION).value

        result = courier.move(ORDER_LOCATION)

        assert result.is_success
        assert courier.location == Location.create(3, 1).value
