import uuid

from python.helpers import create_location, create_speed, create_volume

BASKET_ID = uuid.uuid4()
ORDER_LOCATION = create_location(1, 1)
ORDER_VOLUME = create_volume(10)

COURIER_NAME = "Олег"
COURIER_SPEED = create_speed(2)
COURIER_LOCATION = create_location(5, 5)
