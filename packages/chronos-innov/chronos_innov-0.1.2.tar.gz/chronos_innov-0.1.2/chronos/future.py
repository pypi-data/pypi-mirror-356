from datetime import datetime
from typing import Iterable, List
import random
from .change_algebra import ChangeEvent, ChangeSet

class FutureChangeSet(ChangeSet):
    def __init__(self, events: Iterable[ChangeEvent] | None = None, *, closed: bool = True):
        super().__init__(events)
        self.closed = closed

    def target_events(self) -> List[ChangeEvent]:
        now = 0.0
        return [ev for ev in self if (isinstance(ev.t0, (int, float)) and ev.t0 >= now or isinstance(ev.t0, datetime) and ev.t0 >= datetime.utcnow()) and ev.prob > 0.0]

    def sample_path(self, *, max_events: int = 6, p_floor: float = 0.05) -> "ChangeSet":
        if self.closed:
            raise ValueError("sample_path is only meaningful for open‑ended futures")
        future_events = sorted(self.target_events(), key=lambda e: e.t0)
        chosen = []
        for ev in future_events:
            if ev.prob >= 1.0 or random.random() < ev.prob:
                chosen.append(ev)
                if len(chosen) >= max_events:
                    break
            elif ev.prob < p_floor:
                break
        return ChangeSet(chosen) 