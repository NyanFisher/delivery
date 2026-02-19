import typing
from collections.abc import Iterable

if typing.TYPE_CHECKING:
    from libs.ddd.aggregate import Aggregate


class DomainEventPublisher(typing.Protocol):
    def publish(self, aggregates: Iterable["Aggregate"]) -> None: ...
