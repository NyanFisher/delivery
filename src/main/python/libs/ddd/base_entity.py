from typing import Any


class BaseEntity[TId: Any]:
    def __init__(self, id_: TId | None = None) -> None:
        self._id = id_

    @property
    def id_(self) -> TId | None:
        return self._id

    def _is_transient(self) -> bool:
        return self._id is None or self._id == self._default_value()

    def _default_value(self) -> TId | None:
        return None

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseEntity):
            return NotImplemented

        if self is other:
            return True

        # Проверка на тип. Тип должен быть строго таким же, без наследования.
        if type(self) is not type(other):
            return False

        if self._is_transient() or other._is_transient():
            return False

        return self._id == other._id

    def __hash__(self) -> int:
        return hash((self.__class__.__name__, str(self._id) if self._id is not None else ""))

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, BaseEntity):
            return NotImplemented

        if self is other:
            return False

        if self._is_transient() or other._is_transient():
            return False

        return self._id < other._id  # type: ignore[operator]
