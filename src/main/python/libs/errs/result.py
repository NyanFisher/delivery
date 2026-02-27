from collections.abc import Callable
from typing import Any, cast

from libs.errs.error import DomainInvariantError, Error


class Result[T, E: Error]:
    def __init__(self, value: T | None, error: E | None, is_success: bool) -> None:
        self._value = value
        self._error = error
        self._is_success = is_success

    @classmethod
    def success(cls, value: T) -> "Result[T, Any]":
        if value is None:
            raise ValueError("Value cannot be None for success result")
        return cls(value=value, error=None, is_success=True)

    @classmethod
    def success_void(cls) -> "Result[None, Any]":
        return cls(value=None, error=None, is_success=True)  # type: ignore[return-value]

    @classmethod
    def failure(cls, error: E) -> "Result[Any, E]":
        if error is None:
            raise ValueError("Error cannot be None for failure result")
        return cls(value=None, error=error, is_success=False)

    @property
    def is_success(self) -> bool:
        return self._is_success

    @property
    def is_failure(self) -> bool:
        return not self._is_success

    @property
    def value(self) -> T:
        if not self._is_success:
            raise RuntimeError("Cannot get value from failure")
        return cast("T", self._value)

    @property
    def error(self) -> E:
        if self._is_success:
            raise RuntimeError("Cannot get error from success")
        return cast("E", self._error)

    def map_[U](self, mapper: Callable[[T], U]) -> "Result[U, E]":
        if self._is_success:
            return Result.success(mapper(cast("T", self._value)))
        return Result.failure(cast("E", self._error))

    def flat_map[U](self, mapper: Callable[[T], "Result[U, E]"]) -> "Result[U, E]":
        if self._is_success:
            return mapper(cast("T", self._value))
        return Result.failure(cast("E", self._error))

    def on_success(self, handler: Callable[[T], None]) -> "Result[T, E]":
        if self._is_success:
            handler(cast("T", self._value))
        return self

    def on_failure(self, handler: Callable[[E], None]) -> "Result[T, E]":
        if self.is_failure:
            handler(cast("E", self._error))
        return self

    def fold[U](self, on_success: Callable[[T], U], on_failure: Callable[[E], U]) -> U:
        if self._is_success:
            return on_success(cast("T", self._value))
        return on_failure(cast("E", self._error))

    def map_error[F: Error](self, mapper: Callable[[E], F]) -> "Result[T, F]":
        if self._is_success:
            return Result.success(self._value)  # type: ignore[arg-type]
        return Result.failure(mapper(cast("E", self._error)))

    def get_value_or_throw(self) -> T:
        if self._is_success:
            return cast("T", self._value)
        raise DomainInvariantError(cast("E", self._error))

    def __str__(self) -> str:
        if self._is_success:
            return f"Success({self._value})"
        return f"Failure({cast('E', self._error)})"

    def __repr__(self) -> str:
        return self.__str__()
