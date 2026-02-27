from typing import Final

MIN_LEN_PARTS: Final = 2


class Error:
    SEPARATOR = "||"

    def __init__(self, code: str, message: str) -> None:
        self._code = code
        self._message = message

    @property
    def code(self) -> str:
        return self._code

    @property
    def message(self) -> str:
        return self._message

    def serialize(self) -> str:
        return f"{self._code}{self.SEPARATOR}{self._message}"

    @classmethod
    def deserialize(cls, serialized: str) -> "Error":
        if serialized == "A non-empty request body is required.":
            return GeneralErrors.value_is_required("serialized")

        parts = serialized.split(cls.SEPARATOR)

        if len(parts) < MIN_LEN_PARTS:
            raise ValueError(f"Invalid error serialization: '{serialized}'")

        return cls(parts[0], parts[1])

    @staticmethod
    def throw_if(error: "Error | None") -> None:
        if error is not None:
            raise DomainInvariantError(error)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Error):
            return NotImplemented

        if self is other:
            return True

        return self._code == other._code and self._message == other._message

    def __hash__(self) -> int:
        return hash((self._code, self._message))

    def __repr__(self) -> str:
        return f"Error{{code='{self._code}', message='{self._message}'}}"


class DomainInvariantError[**P](Exception):
    def __init__(self, msg: Error, *args: P.args, **kwargs: P.kwargs) -> None:
        super().__init__(f"Domain invariant violated: {msg}", *args, **kwargs)


class GeneralErrors[T]:
    @staticmethod
    def not_found(name: str, id_: T) -> Error:
        if GeneralErrors._is_null_or_empty(name):
            raise ValueError("Name must not be null or empty")

        return Error("record.not.found", f"Record not found. Name: {name}, id: {id_}")

    @staticmethod
    def value_is_invalid(name: str, value: T) -> Error:
        if GeneralErrors._is_null_or_empty(name):
            raise ValueError("Name must not be null or empty")

        return Error("value.is.invalid", f"Value '{value}' is invalid for {name}")

    @staticmethod
    def value_is_required(name: str) -> Error:
        if GeneralErrors._is_null_or_empty(name):
            raise ValueError("Name must not be null or empty")

        return Error("value.is.required", f"Value is required for {name}")

    @staticmethod
    def invalid_length(name: str) -> Error:
        if GeneralErrors._is_null_or_empty(name):
            raise ValueError("Name must not be null or empty")

        return Error("invalid.string.length", f"Invalid {name} length")

    @staticmethod
    def collection_is_too_small(min_size: int, current_size: int) -> Error:
        return Error(
            "collection.is.too.small",
            f"The collection must contain {min_size} items or more. It contains {current_size} items.",
        )

    @staticmethod
    def collection_is_too_large(max_size: int, current_size: int) -> Error:
        return Error(
            "collection.is.too.large",
            f"The collection must contain {max_size} items or fewer. It contains {current_size} items.",
        )

    @staticmethod
    def value_is_out_of_range(name: str, value: T, min_value: T, max_value: T) -> Error:
        if GeneralErrors._is_null_or_empty(name):
            raise ValueError("Name must not be null or empty")

        message = f"Value {value} for {name} is out of range. Min value is {min_value}, max value is {max_value}."
        return Error("value.is.out.of.range", message)

    @staticmethod
    def value_must_be_greater_than(name: str, value: T, min_value: T) -> Error:
        if GeneralErrors._is_null_or_empty(name):
            raise ValueError("Name must not be null or empty")

        return Error(
            "value.must.be.greater.than",
            f"The value of {name} ({value}) must be greater than {min_value}.",
        )

    @staticmethod
    def value_must_be_greater_or_equal(name: str, value: T, min_value: T) -> Error:
        if GeneralErrors._is_null_or_empty(name):
            raise ValueError("Name must not be null or empty")

        return Error(
            "value.must.be.greater.or.equal",
            f"The value of {name} ({value}) must be greater than or equal to {min_value}.",
        )

    @staticmethod
    def value_must_be_less_than(name: str, value: T, max_value: T) -> Error:
        if GeneralErrors._is_null_or_empty(name):
            raise ValueError("Name must not be null or empty")

        return Error(
            "value.must.be.less.than",
            f"The value of {name} ({value}) must be less than {max_value}.",
        )

    @staticmethod
    def value_must_be_less_or_equal(name: str, value: T, max_value: T) -> Error:
        if GeneralErrors._is_null_or_empty(name):
            raise ValueError("Name must not be null or empty")

        return Error(
            "value.must.be.less.or.equal",
            f"The value of {name} ({value}) must be less than or equal to {max_value}.",
        )

    @staticmethod
    def _is_null_or_empty(s: str) -> bool:
        return s is None or s.strip() == ""
