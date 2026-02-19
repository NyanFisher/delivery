import uuid
from datetime import UTC, datetime
from typing import Any


class DomainEvent:
    def __init__(self, source: Any = None) -> None:  # noqa: ANN401
        self._event_id = uuid.uuid4()
        self._occurred_on_utc = datetime.now(tz=UTC)
        self.source = source
