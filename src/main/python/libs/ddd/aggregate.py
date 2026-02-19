from abc import ABC

from libs.ddd.aggregate_root import AggregateRoot
from libs.ddd.base_entity import BaseEntity
from libs.ddd.domain_event import DomainEvent


class Aggregate[TId](ABC, BaseEntity[TId], AggregateRoot[TId]):
    def __init__(self, id_: TId | None = None) -> None:
        super().__init__(id_)
        self._domain_events: list[DomainEvent] = []

    def get_domain_events(self) -> list[DomainEvent]:
        return self._domain_events.copy()

    def clear_domain_events(self) -> None:
        self._domain_events.clear()

    def raise_domain_event(self, domain_event: DomainEvent) -> None:
        self._domain_events.append(domain_event)
