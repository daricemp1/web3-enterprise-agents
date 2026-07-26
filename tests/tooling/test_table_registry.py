"""Guards against duplicate agent_ids in the shared table registry — a collision here would
silently defeat the table-name-prefixing collision prevention the registry exists for
(see _shared/table_registry.yaml's header comment).
"""
from pathlib import Path

import yaml

REGISTRY_PATH = Path(__file__).resolve().parents[2] / "_shared" / "table_registry.yaml"


def test_every_agent_has_a_nonempty_agent_id():
    registry = yaml.safe_load(REGISTRY_PATH.read_text())

    for agent_name, entry in registry["agents"].items():
        assert entry.get("agent_id"), f"Agent '{agent_name}' is missing an agent_id in {REGISTRY_PATH}"


def test_all_agent_ids_are_unique_across_every_domain():
    registry = yaml.safe_load(REGISTRY_PATH.read_text())
    agent_ids = [entry["agent_id"] for entry in registry["agents"].values()]

    assert len(agent_ids) == len(set(agent_ids)), (
        f"Duplicate agent_id in {REGISTRY_PATH}: {agent_ids} — "
        "table names would collide across agents despite prefixing"
    )
