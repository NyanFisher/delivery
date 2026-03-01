from collections.abc import Callable
from typing import Any, cast

from .error import DomainInvariantError, Error
from .result import Result


class UnitResult[E: Error]:
    def __init__(self, is_success: bool, error: E | None) -> None:
        self._is_success = is_success
        self._error = error

    @classmethod
    def success(cls) -> "UnitResult[Any]":
        return cls(is_success=True, error=None)

    @classmethod
    def failure(cls, error: E) -> "UnitResult[E]":
        if error is None:
            raise ValueError("Error must not be None for failure")
        return cls(is_success=False, error=error)

    @property
    def is_success(self) -> bool:
        return self._is_success

    @property
    def is_failure(self) -> bool:
        return not self._is_success

    @property
    def error(self) -> E:
        if self._is_success:
            raise RuntimeError("Cannot get error from success")
        return cast("E", self._error)

    def on_success(self, handler: Callable[[], None]) -> "UnitResult[E]":
        if self._is_success:
            handler()
        return self

    def on_failure(self, handler: Callable[[E], None]) -> "UnitResult[E]":
        if self.is_failure:
            handler(cast("E", self._error))
        return self

    def fold[U](
        self,
        on_success: Callable[[None], U],
        on_failure: Callable[[E], U],
    ) -> U:
        if self._is_success:
            return on_success(None)
        return on_failure(cast("E", self._error))

    def merge(self, other: "UnitResult[E]") -> "UnitResult[E]":
        if self.is_failure:
            return self
        if other.is_failure:
            return other
        return UnitResult.success()

    @classmethod
    def from_result(cls, result: Result[None, E]) -> "UnitResult[E]":
        return cls.success() if result.is_success else cls.failure(result.error)

    def to_result(self) -> Result[None, E]:
        if self.is_failure:
            return Result.failure(cast("E", self._error))
        return Result.success_void()

    def get_or_else_throw(self, exception_mapper: Callable[[E], Exception] | None = None) -> None:
        if self._is_success:
            return
        if exception_mapper is not None:
            raise exception_mapper(cast("E", self._error))
        raise DomainInvariantError(cast("E", self._error))

    def __str__(self) -> str:
        if self._is_success:
            return "Success"
        return f"Failure({cast('E', self._error)})"

    def __repr__(self) -> str:
        return self.__str__()
