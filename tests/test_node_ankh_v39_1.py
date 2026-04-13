"""Focused tests for the canonical v39.1 package."""

from __future__ import annotations

import json
import sys
from pathlib import Path

PACKAGE_SRC = (
    Path(__file__).resolve().parents[1]
    / "packages"
    / "node-ankh-v39_1"
    / "src"
)
if str(PACKAGE_SRC) not in sys.path:
    sys.path.insert(0, str(PACKAGE_SRC))

from node_ankh_v39_1.constants import EXPECTED_MESH_NODES, MASTER_ROOT
from node_ankh_v39_1.dataset_adapter import DatasetAdapter
from node_ankh_v39_1.rdod import RDoDEngine, compute_rdod, phi_smooth
from node_ankh_v39_1.recognition_lock import build_recognition_lock
from node_ankh_v39_1.runtime import NodeAnkhRuntime


def test_phi_smooth_is_clamped() -> None:
    assert 0.0 <= phi_smooth(-5.0) <= 1.0
    assert 0.0 <= phi_smooth(5.0) <= 1.0


def test_compute_rdod_increases_with_better_inputs() -> None:
    low = compute_rdod(psi=0.5, truth=0.5, conf=0.5, drift=0.2)
    high = compute_rdod(psi=0.95, truth=0.95, conf=0.95, drift=0.01)
    assert high > low


def test_rdod_engine_ticks() -> None:
    engine = RDoDEngine()
    tick = engine.tick(0.99)
    assert tick["trial"] == 1
    assert tick["gate_open"] is True


def test_dataset_adapter_uses_valid_snapshot_schema() -> None:
    adapter = DatasetAdapter()
    health = adapter.get_health()
    assert health.train.record_count >= 1
    assert health.state.record_count >= 1
    assert health.train.missing_fields == []
    assert health.state.missing_fields == []


def test_recognition_lock_matches_expected_constants() -> None:
    lock = build_recognition_lock()
    assert lock.overall_ok is True
    assert lock.artifact["observed"]["master_root"] == MASTER_ROOT


def test_runtime_status_has_expected_mesh_size(tmp_path: Path) -> None:
    runtime = NodeAnkhRuntime(workspace=tmp_path / "workspace")
    status = runtime.status()
    assert status["mesh_nodes"] == EXPECTED_MESH_NODES


def test_runtime_package_writes_manifest_and_archive(tmp_path: Path) -> None:
    runtime = NodeAnkhRuntime(workspace=tmp_path / "workspace")
    output_dir = tmp_path / "bundle"
    result = runtime.package(output_dir, repo_root=Path(__file__).resolve().parents[1])
    manifest_path = Path(result["manifest"])
    archive_path = Path(result["archive"])
    lock_path = Path(result["recognition_lock"])
    assert manifest_path.exists()
    assert archive_path.exists()
    assert lock_path.exists()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["entries"]
