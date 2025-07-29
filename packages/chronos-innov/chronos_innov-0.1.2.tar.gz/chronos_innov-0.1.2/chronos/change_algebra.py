"""chronos SDK — change_algebra module
Defines the basic ChangeEvent data structure and ChangeSet algebra
(union, intersection, difference, composition, inverse, state evolution).
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, Iterable, List, Any
import itertools

@dataclass(frozen=True, order=True)
class ChangeEvent:
    eid: str
    t0: float | datetime
    dt: float = 0.0
    prob: float = 1.0
    meta: Dict[str, Any] | None = field(default_factory=dict)

    @property
    def t1(self) -> float | datetime:
        if isinstance(self.t0, datetime):
            return self.t0 + timedelta(days=self.dt)
        return self.t0 + self.dt

    def with_prob(self, p: float) -> "ChangeEvent":
        return ChangeEvent(self.eid, self.t0, self.dt, p, self.meta)

class ChangeSet:
    def __init__(self, events: Iterable[ChangeEvent] | None = None):
        self._events: Dict[str, ChangeEvent] = {}
        if events:
            for ev in events:
                self.add(ev)

    def add(self, ev: ChangeEvent) -> None:
        self._events[ev.eid] = ev

    def discard(self, eid: str) -> None:
        self._events.pop(eid, None)

    def union(self, other: "ChangeSet") -> "ChangeSet":
        return ChangeSet(itertools.chain(self._events.values(), other._events.values()))

    def intersection(self, other: "ChangeSet") -> "ChangeSet":
        return ChangeSet(ev for ev in self if ev.eid in other._events)

    def difference(self, other: "ChangeSet") -> "ChangeSet":
        return ChangeSet(ev for ev in self if ev.eid not in other._events)

    def ordered(self, by: str = "t0") -> List[str]:
        return [ev.eid for ev in sorted(self, key=lambda e: getattr(e, by))]

    def __iter__(self):
        return iter(self._events.values())

    def __len__(self):
        return len(self._events)

    def __contains__(self, eid: str):
        return eid in self._events

    def __repr__(self):
        return f"ChangeSet({list(self._events)})" 