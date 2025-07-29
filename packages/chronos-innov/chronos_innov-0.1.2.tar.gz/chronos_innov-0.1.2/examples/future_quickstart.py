"""
future_quickstart.py – A Whimsical Tour of Probabilistic Futures

Welcome to the Infinite Improbability Drive demo! Here, timelines are as likely as a bowl of petunias falling from the sky. Let's see which improbable product launches the universe coughs up today...
"""
from chronos.change_algebra import ChangeEvent
from chronos.future import FutureChangeSet
from chronos.manifold import InnovationMetric
from chronos.navigator import Navigator

# ── 1. Engage the Improbability Drive: define quantum events ─────────────
idea = ChangeEvent("idea-drafted", t0:=0, dt:=0.1, prob=1.0)
tea_party = ChangeEvent("tea-party-with-Vogon", t0+1, dt=0.5, prob=0.7)
whale = ChangeEvent("spontaneous-whale-appearance", t0+2, dt=0.2, prob=0.3)
petunias = ChangeEvent("petunia-uprising", t0+3, dt=0.1, prob=0.15)

# Branching weirdness
babel_fish = ChangeEvent("babel-fish-in-ear", t0+1.5, dt=0.05, prob=0.5)
poetry = ChangeEvent("forced-to-hear-Vogon-poetry", t0+2.5, dt=0.3, prob=0.1)
towel = ChangeEvent("towel-misplaced", t0+4, dt=0.05, prob=0.05)

future_timeline = FutureChangeSet([
    idea, tea_party, whale, petunias, babel_fish, poetry, towel
], closed=False)

print("\n🚀 Improbability Matrix Initialized! Possible events in the quantum soup:")
for ev in future_timeline:
    print(f"  • {ev.eid} (probability: {ev.prob:.2f})")

# ── 2. Set the metric tensor to 'mostly harmless' ───────────────────────
metric = InnovationMetric(weight_time=1.0, weight_scope=1.5, weight_risk=2.0)
nav = Navigator(metric)

# ── 3. Ask the Drive for the 3 most improbable probable futures ──────────
scenarios = nav.enumerate_scenarios(future_timeline, n=3)

for i, path in enumerate(scenarios, 1):
    eids = path.ordered()
    joint_prob = 1.0
    for eid in eids:
        joint_prob *= future_timeline._events[eid].prob
    print(f"\n✨ Scenario {i}: Improbability Quotient = {joint_prob:.3f}")
    print(nav.pretty_report(eids))
    if "petunia-uprising" in eids:
        print("  (Alert: The petunias are organizing. Don't panic.)")
    if "spontaneous-whale-appearance" in eids:
        print("  (A whale has materialized. It seems confused.)")
    if "forced-to-hear-Vogon-poetry" in eids:
        print("  (Brace yourself. The poetry is coming.)")
    if joint_prob < 0.2:
        print("  (Warning: This scenario may spontaneously turn into a whale or a bowl of petunias.)") 