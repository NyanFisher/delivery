import typing
from dataclasses import dataclass, field

from libs.errs.guard import Error, Guard
from libs.errs.result import Result


@dataclass(frozen=True)
class Location:
    MIN_VALUE: typing.Final[int] = field(default=1, init=False, repr=False, compare=False)
    MAX_VALUE: typing.Final[int] = field(default=10, init=False, repr=False, compare=False)

    x: int
    y: int

    @classmethod
    def create(cls, x: int, y: int) -> Result[typing.Self, Error]:
        if err := Guard.against_out_of_range(x, cls.MIN_VALUE, cls.MAX_VALUE, param_name="x"):
            return Result.failure(err)
        if err := Guard.against_out_of_range(y, cls.MIN_VALUE, cls.MAX_VALUE, param_name="y"):
            return Result.failure(err)

        return Result.success(cls(x=x, y=y))

    def distance_to(self, location: "Location") -> int:
        return abs(self.x - location.x) + abs(self.y - location.y)
