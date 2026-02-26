from abc import ABC, abstractmethod
from collections.abc import Iterable
from decimal import Decimal
from typing import Any


class ValueObject[T](ABC):
    @abstractmethod
    def _equality_components(self) -> Iterable[Any]: ...

    @staticmethod
    def _safe_compare[V: (int, float, str, bool, Decimal)](a: V, b: V) -> int:  # noqa: PLR0911
        if a == b:
            return 0
        if a is None:
            return -1
        if b is None:
            return 1

        if isinstance(a, Decimal) and isinstance(b, Decimal):
            return int(a.compare(b))

        if not isinstance(a, (int, float, str, bool, Decimal)) or not isinstance(b, (int, float, str, bool, Decimal)):
            raise TypeError("Fields must be comparable types")

        if a < b:
            return -1
        if a > b:
            return 1
        return 0

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ValueObject):
            return NotImplemented

        if self is other:
            return True

        this_components = list(self._equality_components())
        that_components = list(other._equality_components())

        if len(this_components) != len(that_components):
            return False

        return all(component == that_components[i] for i, component in enumerate(this_components))

    def __hash__(self) -> int:
        return hash(tuple(self._equality_components()))

    def __lt__(self, other: T) -> bool:
        if not isinstance(other, ValueObject):
            return NotImplemented

        this_components = list(self._equality_components())
        other_components = list(other._equality_components())

        for i in range(min(len(this_components), len(other_components))):
            result = self._safe_compare(this_components[i], other_components[i])
            if result != 0:
                return result < 0

        return len(this_components) < len(other_components)

    def __str__(self) -> str:
        components = list(self._equality_components())
        components_str = ", ".join(str(component) for component in components)
        return f"{self.__class__.__name__}[{components_str}]"
