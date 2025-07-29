"""chronos SDK — trust module
Weighted directed graph of trust coefficients with simple logistic update law.
Requires the optional **networkx** package for graph operations.
"""

from collections import defaultdict
from typing import Dict, Iterable

class TrustGraph:
    def __init__(self):
        self._g: Dict[str, Dict[str, float]] = defaultdict(dict)

    def add_node(self, actor: str) -> None:
        _ = self._g[actor]

    def add_researchers(self, actors: Iterable[str]):
        for a in actors:
            self.add_node(a)

    def set_trust(self, src: str, dst: str, weight: float):
        self._g[src][dst] = max(0.0, min(1.0, weight))

    def edge_weights(self):
        return {(s, d): w for s, nbr in self._g.items() for d, w in nbr.items()}

    def trust_boost(self, src: str, dst: str) -> float:
        w = self._g.get(src, {}).get(dst, 0.0)
        return 1.0 + w 