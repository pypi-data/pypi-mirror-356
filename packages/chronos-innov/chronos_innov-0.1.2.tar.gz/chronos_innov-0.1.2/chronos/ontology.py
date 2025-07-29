from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Callable
from .change_algebra import ChangeEvent, ChangeSet

@dataclass(frozen=True)
class Schema:
    type_id: str
    mean_period: float
    default_dt: float = 0.0
    description: str = ""
    meta: Dict[str, Any] | None = field(default_factory=dict)

class Ontology:
    def __init__(self):
        self._schemas: Dict[str, Schema] = {}
        self._entities: Dict[str, "Entity"] = {}

    def add_schema(self, schema: Schema):
        if schema.type_id in self._schemas:
            raise KeyError(f"Schema '{schema.type_id}' already exists")
        self._schemas[schema.type_id] = schema

    def schema(self, type_id: str) -> Schema:
        return self._schemas[type_id]

    def spawn(self,
              entity_id: str,
              type_id: str,
              goal_name: str,
              generator_fn: Callable[["Entity"], ChangeSet],
              *,
              t0: float | datetime = 0.0,
              priority: int = 0) -> "Entity":
        if entity_id in self._entities:
            raise KeyError(f"Entity '{entity_id}' already exists")
        schema = self.schema(type_id)
        goal_eid = f"{entity_id}::goal::{goal_name}"
        goal_ev = ChangeEvent(goal_eid, t0, dt=0.0, prob=1.0, meta={"priority": priority})
        timeline = ChangeSet()
        ent = Entity(entity_id, schema, goal_ev, timeline, generator_fn, priority)
        timeline.add(goal_ev)
        timeline = generator_fn(ent) or timeline
        ent.timeline = timeline
        self._entities[entity_id] = ent
        return ent

    def entities(self):
        return list(self._entities.values())

@dataclass
class Entity:
    eid: str
    schema: Schema
    goal: ChangeEvent
    timeline: ChangeSet
    generator: Callable[["Entity"], ChangeSet]
    priority: int = 0

    def regenerate(self):
        self.timeline = self.generator(self) or self.timeline 