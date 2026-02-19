import typing

from libs.ddd.domain_event import DomainEvent


class AggregateRoot[ID](typing.Protocol):
    def get_id(self) -> ID: ...

    def get_domain_events(self) -> list[DomainEvent]: ...

    def clear_domain_events(self) -> None: ...
