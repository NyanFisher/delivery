import typing
from collections.abc import Iterable

from libs.ddd.value_object import ValueObject
from libs.errs.guard import Error, Guard
from libs.errs.result import Result


class Location(ValueObject["Location"]):
    MIN_VALUE: typing.Final = 1
    MAX_VALUE: typing.Final = 10

    def __init__(self, x: int, y: int) -> None:
        self._x = x
        self._y = y

    def __repr__(self) -> str:
        return f"Location(x={self.x}, y={self.y})"

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @classmethod
    def create(cls, x: int, y: int) -> Result[typing.Self, Error]:
        if err := Guard.against_out_of_range(x, cls.MIN_VALUE, cls.MAX_VALUE, param_name="x"):
            return Result.failure(err)
        if err := Guard.against_out_of_range(y, cls.MIN_VALUE, cls.MAX_VALUE, param_name="y"):
            return Result.failure(err)

        return Result.success(cls(x=x, y=y))

    def distance_to(self, location: "Location") -> int:
        return abs(self.x - location.x) + abs(self.y - location.y)

    def _equality_components(self) -> Iterable[int]:
        return (self.x, self.y)
