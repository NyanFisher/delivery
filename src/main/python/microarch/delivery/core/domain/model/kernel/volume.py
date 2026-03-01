import typing
from dataclasses import dataclass, field

from libs.errs import Error, Guard, Result


@dataclass(frozen=True, order=True)
class Volume:
    # Do not call the constructor directly. Use the `create` method to create.
    MIN_TOTAL_VOLUME: typing.Final[int] = field(default=1, repr=False, init=False, compare=False)

    value: int

    @classmethod
    def create(cls, value: int) -> Result[typing.Self, Error]:
        if err := Guard.against_less_than(value, cls.MIN_TOTAL_VOLUME, "value"):
            return Result.failure(err)
        return Result.success(cls(value=value))
