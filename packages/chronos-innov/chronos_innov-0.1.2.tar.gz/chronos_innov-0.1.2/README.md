# chronos

Chronos: Innovation Algebra & Trust SDK
=======================================

A minimal, composable Python SDK for modeling change events, trust graphs, and innovation landscapes. Includes algebraic change sets, trust propagation, Riemannian geometry helpers, and a master equation integrator.

## Features
- **Change Algebra**: Immutable, timestamped change events and sets with union/intersection/difference, composition, inversion, and state evolution.
- **Trust Graphs**: Weighted directed trust networks with path aggregation and logistic update law (requires `networkx`).
- **Manifold Geometry**: Minimal Riemannian metric/geodesic/curvature helpers (requires `numpy`).
- **Navigator**: Lightweight forward-Euler integrator for arbitrary vector fields.
- **Future Layer**: Probabilistic, open-ended futures with `FutureChangeSet` and scenario enumeration.
- **Ontology Layer**: Reusable change schemas and goal-driven entities with `Schema`, `Ontology`, and `Entity`.

## Installation

With [UV](https://github.com/astral-sh/uv):
```sh
uv pip install chronos-innov
```

Or with pip:
```sh
pip install chronos-innov
```

## Usage

### Change Algebra
```python
from chronos import ChangeEvent, ChangeSet, change_set

# Create events
c1 = ChangeEvent(timestamp=1.0, state_before=0, state_after=1)
c2 = ChangeEvent(timestamp=2.0, state_before=1, state_after=2)

# Create a set
cs = ChangeSet([c1, c2])

# Algebraic ops
cs2 = cs.inverse()
cs3 = cs.union(cs2)
```

### Trust Graphs
```python
from chronos import TrustGraph
T = TrustGraph()
T.set_trust('alice', 'bob', 0.8)
T.update_trust('alice', 'bob', delta=0.1)
trust = T.get_trust('alice', 'bob')
```

### Manifold Geometry
```python
from chronos import Metric, geodesic, curvature
import numpy as np
metric = Metric(lambda x: np.eye(len(x)))
path = geodesic(metric, np.array([0,0]), np.array([1,1]))
curv = curvature(metric, np.array([0,0]))
```

### Navigator
```python
from chronos import Navigator
import numpy as np
nav = Navigator(lambda x: -x)
traj = nav.integrate(np.array([1.0, 0.0]), steps=10)
```

### Future Layer
```python
from chronos import ChangeEvent, FutureChangeSet, Navigator

# Define probabilistic future events
idea = ChangeEvent("idea-drafted", t0=0, dt=0.1, prob=1.0)
tea_party = ChangeEvent("tea-party-with-Vogon", t0=1, dt=0.5, prob=0.7)
whale = ChangeEvent("spontaneous-whale-appearance", t0=2, dt=0.2, prob=0.3)
petunias = ChangeEvent("petunia-uprising", t0=3, dt=0.1, prob=0.15)

future_timeline = FutureChangeSet([idea, tea_party, whale, petunias], closed=False)

# Enumerate top 3 most probable future scenarios
nav = Navigator(InnovationMetric())
scenarios = nav.enumerate_scenarios(future_timeline, n=3)
for i, path in enumerate(scenarios, 1):
    print(f"Scenario {i}: {path.ordered()}")
```

### Ontology Layer
```python
from chronos import Schema, Ontology, Entity, Navigator

# Define a schema
feature_schema = Schema("feature", mean_period=5.0, default_dt=1.0, description="A new feature")

# Create an ontology and add the schema
onto = Ontology()
onto.add_schema(feature_schema)

# Spawn an entity with a goal
def my_generator(entity):
    return ChangeSet([ChangeEvent("my-goal", t0=0, dt=0.1, prob=1.0)])

entity = onto.spawn("my_entity", "feature", "my-goal", my_generator)

# Use Navigator to find a path to the entity's goal
nav = Navigator(InnovationMetric())
path, total = nav.entity_goal_path(entity)
print(nav.pretty_report(path))
```

## Requirements
- Python 3.9+
- `networkx` (for trust graphs)
- `numpy` (for manifold & navigator)

---
MIT License. See source for details.