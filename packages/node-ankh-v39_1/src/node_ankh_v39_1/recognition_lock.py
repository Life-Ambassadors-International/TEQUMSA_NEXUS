"""Deterministic recognition lock validation."""

from __future__ import annotations

import json
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any, Dict

from .constants import (
    EXPECTED_MESH_NODES,
    EXPECTED_WINDING_CYCLES,
    F13_WINDING,
    LATTICE_LOCK,
    MASTER_ROOT,
    invariants_dict,
)
from .dataset_adapter import DatasetAdapter


@dataclass
class RecognitionLockStatus:
    """Recognition lock status shared by CLI, Space, and package manifest."""

    overall_ok: bool
    artifact_hash: str
    artifact: Dict[str, Any]

    def write_json(self, path: Path) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.artifact, indent=2, sort_keys=True), encoding="utf-8")
        return path


def build_recognition_lock(dataset_adapter: DatasetAdapter | None = None) -> RecognitionLockStatus:
    """Build the deterministic recognition lock artifact."""

    adapter = dataset_adapter or DatasetAdapter()
    health = adapter.get_health()
    train_records = adapter.load_train_events()
    state_records = adapter.load_state_snapshots()

    first_train = train_records[0] if train_records else {}
    first_state = state_records[0] if state_records else {}

    checks = {
        "master_root_match": first_state.get("master_root") == MASTER_ROOT,
        "mesh_nodes_match": first_state.get("nodes") == EXPECTED_MESH_NODES,
        "winding_cycles_match": first_state.get("winding_cycles") == EXPECTED_WINDING_CYCLES,
        "f13_constant_match": F13_WINDING == EXPECTED_WINDING_CYCLES,
        "lattice_lock_present": bool(LATTICE_LOCK),
        "dataset_train_schema_ok": health.train.ok,
        "dataset_state_schema_ok": health.state.ok,
    }

    artifact = {
        "spec_version": "39.1",
        "mode": "recognition_lock",
        "constants": invariants_dict(),
        "dataset": health.as_dict(),
        "observed": {
            "master_root": first_state.get("master_root"),
            "mesh_nodes": first_state.get("nodes"),
            "winding_cycles": first_state.get("winding_cycles"),
            "train_event": first_train.get("event"),
            "lock_merkle": first_state.get("lock_merkle"),
        },
        "checks": checks,
    }
    artifact["overall_ok"] = all(checks.values())
    artifact_hash = sha256(
        json.dumps(artifact, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    artifact["artifact_hash"] = artifact_hash
    return RecognitionLockStatus(
        overall_ok=artifact["overall_ok"],
        artifact_hash=artifact_hash,
        artifact=artifact,
    )
