"""
quickstart.py  –  A five-minute tour of the Chrono-Innov SDK
Scenario: a product team wants to forecast the fastest credible path
from an idea (“Smart Checklist”) to public launch, given both
technical work and verification lead-times that depend on TRUST.
"""

# ── 0. Imports ──────────────────────────────────────────────────────
from chronos.change_algebra import ChangeEvent, ChangeSet
from chronos.trust           import TrustGraph
from chronos.manifold        import InnovationMetric
from chronos.navigator       import Navigator

# ── 1. Build a ChangeSet (raw timeline of work) ─────────────────────
idea       = ChangeEvent("idea-drafted",    t0:=0,   dt:=0.5)  # days
prototype  = ChangeEvent("prototype-done",  t0+2,    1.0)
usertest   = ChangeEvent("usertest-closed", t0+5,    0.5)
launch     = ChangeEvent("launch-live",     t0+12,   0.1)

timeline = ChangeSet([idea, prototype, usertest, launch])
print("❖ raw timeline:", timeline.ordered())

# ── 2. Encode social capital that speeds (or slows) verification ────
g = TrustGraph()
g.add_researchers(["Alice-QA", "Bob-Legal", "Chloe-PM"])
g.set_trust("Alice-QA",  "Bob-Legal",  0.60)  # moderate trust
g.set_trust("Chloe-PM",  "Alice-QA",   0.85)  # strong trust
g.set_trust("Bob-Legal", "Chloe-PM",   0.30)  # weak trust

print("❖ trust heat-map:", g.edge_weights())

# ── 3. Pick a metric tensor that defines “innovation distance” ──────
metric = InnovationMetric(weight_time=1.0,
                          weight_scope=1.5,
                          weight_risk =2.0)

# ── 4. Solve the optimal (geodesic) route through the work manifold ─
nav = Navigator(metric, g)
path, tmin = nav.shortest_time_path(timeline,
                                    src="idea-drafted",
                                    dst="launch-live")

print(f"🚀 Fastest credible route = {path}  (elapsed ≈ {tmin:.1f} days)")

# ── 5. Produce a teeny report ───────────────────────────────────────
print(nav.pretty_report(path))
