"""chronos SDK — manifold geometry utilities
Minimal Riemannian helpers (metric, geodesic, curvature) for innovation landscapes.
"""

import math

class InnovationMetric:
    def __init__(self, weight_time=1.0, weight_scope=1.0, weight_risk=1.0):
        self.wt, self.ws, self.wr = weight_time, weight_scope, weight_risk

    def distance(self, dtime: float, dscope: float = 0.0, drisk: float = 0.0) -> float:
        return math.sqrt(self.wt * dtime * dtime + self.ws * dscope * dscope + self.wr * drisk * drisk) 