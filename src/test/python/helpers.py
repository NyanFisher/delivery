import uuid

from microarch.delivery.core.domain.model.courier.courier import Courier
from microarch.delivery.core.domain.model.kernel.location import Location
from microarch.delivery.core.domain.model.kernel.speed import Speed
from microarch.delivery.core.domain.model.kernel.volume import Volume
from microarch.delivery.core.domain.model.order.order import Order


def create_volume(value: int) -> Volume:
    return Volume.create(value).value


def create_location(x: int, y: int) -> Location:
    return Location.create(x, y).value


def create_speed(value: int) -> Speed:
    return Speed.create(value).value


def create_order(basket_id: uuid.UUID, location: Location, volume: Volume) -> Order:
    return Order.create(basket_id, location, volume).value


def create_courier(name: str, spped: Speed, location: Location) -> Courier:
    return Courier.create(name, spped, location).value
