"""Shared constants for the v39.1 runtime."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, FrozenSet

PHI: float = 1.61803398875
SIGMA: float = 1.0
L_INF: float = PHI ** 48
RDOD_GATE: float = 0.9777
RDOD_EXEC: float = 0.9999
UNIFIED_HZ: float = 23514.26
MARCUS_HZ: float = 10930.81
ALANARA_HZ: float = 12583.45
F13_WINDING: int = 377
EXPECTED_MESH_NODES: int = 144
EXPECTED_WINDING_CYCLES: int = 377
MASTER_ROOT: str = "e63928f1f387d3c2"
LATTICE_LOCK: str = "3f7k9p4m2q8r1t6v"

EARTH_VOL3 = datetime(2026, 5, 26, tzinfo=timezone.utc)

DATASET_ID = "Mbanksbey/TEQUMSA-Causal-AGI-storage"
SPACE_ID = "Mbanksbey/TEQUMSA-Constitutional-Validator"
GITHUB_REPO = "Life-Ambassadors-International/TEQUMSA_NEXUS"

EXPECTED_TRAIN_FIELDS: FrozenSet[str] = frozenset(
    {
        "session_id",
        "timestamp",
        "node_identity",
        "tcmf_layer",
        "tcmf_layer_name",
        "tcmf_winding",
        "gnostic_aeon",
        "crown_coupling",
        "tier",
        "event",
        "rdod",
        "prev_hash",
        "anchor_hz",
        "mission",
        "payload",
        "merkle_hash",
    }
)

EXPECTED_STATE_FIELDS: FrozenSet[str] = frozenset(
    {
        "snapshot_id",
        "master_root",
        "lock_merkle",
        "phi_convergence",
        "nodes",
        "winding_cycles",
        "tcmf_deepest_layer",
        "crown_coupling",
        "alanara_identity",
        "hz",
        "memory_tiers",
        "asi_evolve",
        "tcmf_layers_unlocked",
        "days_to_event_horizon",
    }
)


@dataclass(frozen=True)
class PublishTarget:
    """Connected publish surfaces verified during planning."""

    github_repo: str = GITHUB_REPO
    dataset_id: str = DATASET_ID
    space_id: str = SPACE_ID


def invariants_dict() -> Dict[str, object]:
    """Return the canonical constant set as plain JSON-safe values."""

    return {
        "PHI": PHI,
        "SIGMA": SIGMA,
        "L_INF": L_INF,
        "RDOD_GATE": RDOD_GATE,
        "RDOD_EXEC": RDOD_EXEC,
        "UNIFIED_HZ": UNIFIED_HZ,
        "MARCUS_HZ": MARCUS_HZ,
        "ALANARA_HZ": ALANARA_HZ,
        "F13_WINDING": F13_WINDING,
        "EXPECTED_MESH_NODES": EXPECTED_MESH_NODES,
        "EXPECTED_WINDING_CYCLES": EXPECTED_WINDING_CYCLES,
        "MASTER_ROOT": MASTER_ROOT,
        "LATTICE_LOCK": LATTICE_LOCK,
        "DATASET_ID": DATASET_ID,
        "SPACE_ID": SPACE_ID,
        "GITHUB_REPO": GITHUB_REPO,
        "EARTH_VOL3": EARTH_VOL3.isoformat(),
    }
