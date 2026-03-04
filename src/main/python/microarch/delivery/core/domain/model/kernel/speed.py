import typing
from dataclasses import dataclass, field

from libs.errs import Error, Guard, Result


@dataclass(frozen=True, order=True)
class Speed:
    # Do not call the constructor directly. Use the `create` method to create.
    MIN_SPEED: typing.Final[int] = field(default=1, init=False, repr=False, compare=False)

    value: int

    @classmethod
    def create(cls, value: int) -> Result[typing.Self, Error]:
        if err := Guard.against_less_than(value, cls.MIN_SPEED, "value"):
            return Result.failure(err)

        return Result.success(cls(value=value))
