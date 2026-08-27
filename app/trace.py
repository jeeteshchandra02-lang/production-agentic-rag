import time
import uuid
from dataclasses import dataclass, field


@dataclass
class TraceEvent:
    name: str
    started_at: float
    duration_ms: float | None = None
    data: dict = field(default_factory=dict)


class Trace:
    def __init__(self):
        self.trace_id = uuid.uuid4().hex
        self.events: list[TraceEvent] = []

    def record(self, name: str, started_at: float, **data):
        duration_ms = (time.perf_counter() - started_at) * 1000
        self.events.append(
            TraceEvent(
                name=name,
                started_at=started_at,
                duration_ms=round(duration_ms, 2),
                data=data,
            )
        )
