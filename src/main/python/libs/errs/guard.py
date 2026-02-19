import typing
import uuid
from collections.abc import Collection as AbcCollection
from decimal import Decimal

from libs.errs.error import Error, GeneralErrors


class Guard[T: (int, float, str, bool, Decimal)]:
    EMPTY_UUID: typing.Final = uuid.UUID("00000000-0000-0000-0000-000000000000")

    @staticmethod
    def combine(*errors: Error | None) -> Error | None:
        for error in errors:
            if error is not None:
                return error
        return None

    @staticmethod
    def against_null_or_empty(value: str | None, param_name: str) -> Error | None:
        if value is None or not value.strip():
            return GeneralErrors.value_is_required(param_name)
        return None

    @staticmethod
    def against_null_or_empty_collection(collection: AbcCollection[T] | None, param_name: str) -> Error | None:
        if collection is None or len(collection) == 0:
            return GeneralErrors.value_is_required(param_name)
        return None

    @staticmethod
    def against_null_or_empty_uuid(uuid_value: uuid.UUID | None, param_name: str) -> Error | None:
        if uuid_value is None or uuid_value == Guard.EMPTY_UUID:
            return GeneralErrors.value_is_required(param_name)
        return None

    @staticmethod
    def against_greater_than(value: T | None, max_value: T, param_name: str) -> Error | None:
        if value is None or value > max_value:
            return GeneralErrors.value_must_be_less_than(param_name, value, max_value)
        return None

    @staticmethod
    def against_greater_or_equal(value: T | None, max_value: T, param_name: str) -> Error | None:
        if value is None or value >= max_value:
            return GeneralErrors.value_must_be_less_or_equal(param_name, value, max_value)
        return None

    @staticmethod
    def against_less_than(value: T | None, min_value: T, param_name: str) -> Error | None:
        if value is None or value < min_value:
            return GeneralErrors.value_must_be_greater_or_equal(param_name, value, min_value)
        return None

    @staticmethod
    def against_less_or_equal(value: T | None, min_value: T, param_name: str) -> Error | None:
        if value is None or value <= min_value:
            return GeneralErrors.value_must_be_greater_or_equal(param_name, value, min_value)
        return None

    @staticmethod
    def against_out_of_range(value: T | None, min_value: T, max_value: T, param_name: str) -> Error | None:
        if value is None or value < min_value or value > max_value:
            return GeneralErrors.value_is_out_of_range(param_name, value, min_value, max_value)
        return None
