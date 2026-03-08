import pytest
from microarch.delivery.core.domain.services.order_dispatcher import OrderDispatcher

from python.constants import BASKET_ID, COURIER_LOCATION, COURIER_NAME, COURIER_SPEED, ORDER_LOCATION, ORDER_VOLUME
from python.helpers import create_courier, create_order, create_speed


class TestOrderDispatcher:
    @pytest.fixture
    def sut(self) -> OrderDispatcher:
        return OrderDispatcher()

    def test_get_error_if_order_is_not_created(self, sut: OrderDispatcher) -> None:
        order = create_order(BASKET_ID, ORDER_LOCATION, ORDER_VOLUME)
        courier = create_courier(COURIER_NAME, COURIER_SPEED, COURIER_LOCATION)
        order.assign(courier)

        result = sut.dispatch(order, couriers=[courier])

        assert result.is_failure
        assert result.error.code == "order.is.not.created"

    def test_get_error_if_list_of_courier_is_empty(self, sut: OrderDispatcher) -> None:
        order = create_order(BASKET_ID, ORDER_LOCATION, ORDER_VOLUME)

        result = sut.dispatch(order, couriers=[])

        assert result.is_failure
        assert result.error.code == "list.of.courier.is.empty"

    def test_get_error_if_there_are_no_suitable_courier(self, sut: OrderDispatcher) -> None:
        order = create_order(BASKET_ID, ORDER_LOCATION, ORDER_VOLUME)
        other_order = create_order(BASKET_ID, ORDER_LOCATION, ORDER_VOLUME)
        courier = create_courier(COURIER_NAME, COURIER_SPEED, COURIER_LOCATION)
        sut.dispatch(other_order, couriers=[courier])

        result = sut.dispatch(order, couriers=[courier])

        assert result.is_failure
        assert result.error.code == "there.are.no.suitable.couriers"

    def test_dispatch_order(self, sut: OrderDispatcher) -> None:
        order = create_order(BASKET_ID, ORDER_LOCATION, ORDER_VOLUME)
        courier_1 = create_courier(COURIER_NAME, COURIER_SPEED, COURIER_LOCATION)
        courier_2 = create_courier(COURIER_NAME, create_speed(2), COURIER_LOCATION)

        result = sut.dispatch(order, couriers=[courier_1, courier_2])

        assert result.is_success
        assert result.value == courier_2
        assert courier_2.storage_places[0].order_id == order.id_
        assert courier_1.storage_places[0].order_id is None
        assert order.courier_id == courier_2.id_
