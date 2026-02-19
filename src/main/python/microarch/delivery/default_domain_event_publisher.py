from collections.abc import Iterable
from typing import Protocol

from libs.ddd.aggregate import Aggregate
from libs.ddd.domain_event import DomainEvent


class ApplicationEventPublisher(Protocol):
    def publish_event(self, event: DomainEvent) -> None: ...


class DefaultDomainEventPublisher:
    def __init__(self, publisher: ApplicationEventPublisher) -> None:
        self.publisher = publisher

    def publish(self, aggregates: Iterable[Aggregate]) -> None:
        for aggregate in aggregates:
            for event in aggregate.get_domain_events():
                self.publisher.publish_event(event)
