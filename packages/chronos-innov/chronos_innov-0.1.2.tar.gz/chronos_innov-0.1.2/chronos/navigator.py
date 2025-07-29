"""chronos SDK — master equation integrator
Lightweight forward‑Euler solver for arbitrary Hamiltonian‑like vector fields.
""" 

from typing import Sequence, List, Tuple
import math
from .manifold import InnovationMetric
from .trust import TrustGraph
from .change_algebra import ChangeSet, ChangeEvent
from .future import FutureChangeSet
from .ontology import Entity

class Navigator:
    """Path‑finding over ChangeSets, FutureChangeSets, and Entities."""

    def __init__(self, metric: InnovationMetric, trust_graph: TrustGraph | None = None):
        self.metric = metric
        self.trust = trust_graph or TrustGraph()

    def shortest_time_path(self, changes: ChangeSet, *, src: str, dst: str) -> Tuple[List[str], float]:
        ordered = [ev for ev in sorted(changes, key=lambda e: e.t0)]
        path_ids = [ev.eid for ev in ordered if ev.eid in {src, dst} or (ev.t0 >= changes._events[src].t0 and ev.t0 <= changes._events[dst].t0)]
        total = sum(ev.dt for ev in ordered if ev.eid in path_ids)
        return path_ids, total

    def entity_goal_path(self, ent: Entity) -> Tuple[List[str], float]:
        """Return a path from *now* to the entity's goal, ordered chronologically."""
        return self.shortest_time_path(ent.timeline, src=min(ent.timeline.ordered(), key=lambda eid: ent.timeline._events[eid].t0), dst=ent.goal.eid)

    def enumerate_scenarios(self, fcs: FutureChangeSet, *, n: int = 3, max_events: int = 6) -> List[ChangeSet]:
        if fcs.closed:
            raise ValueError("enumerate_scenarios expects an *open* FutureChangeSet")
        scenarios = []
        for _ in range(n * 3):
            cs = fcs.sample_path(max_events=max_events)
            prob = math.prod(ev.prob for ev in cs)
            scenarios.append((prob, cs))
        uniq = {}
        for p, cs in scenarios:
            key = tuple(cs.ordered())
            if key not in uniq or p > uniq[key][0]:
                uniq[key] = (p, cs)
        top = sorted(uniq.values(), key=lambda pc: pc[0], reverse=True)[:n]
        return [cs for _, cs in top]

    def pretty_report(self, path: Sequence[str]) -> str:
        lines = ["\n   Chrono‑Innov Navigator – path summary", "   ──────────────────────────────────────"]
        for i, eid in enumerate(path):
            lines.append(f"   {i+1:02d}. {eid}")
        return "\n".join(lines) 