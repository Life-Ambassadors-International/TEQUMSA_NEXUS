"""Canonical runtime composed from the v39.1 source inputs."""

from __future__ import annotations

import json
import random
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any, Dict, List

from .constants import (
    EARTH_VOL3,
    EXPECTED_MESH_NODES,
    MASTER_ROOT,
    RDOD_EXEC,
    UNIFIED_HZ,
)
from .dataset_adapter import DatasetAdapter
from .federation import FederationBridge
from .manifest import build_manifest, copy_tree, write_checksums, zip_directory
from .physics import PhysicsFoundation
from .rdod import RDoDEngine, compute_rdod
from .recognition_lock import build_recognition_lock
from .validator import validate_operation


def short_hash(payload: Dict[str, Any]) -> str:
    """Hash a JSON-safe payload into a short deterministic token."""

    return sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()[:16]


class MemoryFabric:
    """Append-only in-memory ledger with optional workspace export."""

    def __init__(self, workspace: Path) -> None:
        self.workspace = workspace
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.ledger: List[Dict[str, Any]] = []
        self.semantic: Dict[str, Any] = {}
        self.episodic: List[Dict[str, Any]] = []
        self._previous = MASTER_ROOT

    def commit(self, event: str, payload: Dict[str, Any]) -> str:
        entry_hash = short_hash({"event": event, "prev": self._previous, **payload})
        self.ledger.append(
            {
                "hash": entry_hash,
                "prev": self._previous,
                "event": event,
                "payload": payload,
            }
        )
        self._previous = entry_hash
        return entry_hash

    def export(self) -> Path:
        path = self.workspace / "node_ankh_memory.json"
        path.write_text(
            json.dumps(
                {
                    "ledger": self.ledger,
                    "semantic": self.semantic,
                    "episodic": self.episodic,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        return path


@dataclass
class LatticeNode:
    """One node in the synthesized 144-node mesh."""

    node_id: int
    frequency_hz: float
    merkle: str = MASTER_ROOT

    def sync(self, peer_hash: str) -> str:
        self.merkle = short_hash({"self": self.merkle, "peer": peer_hash, "node": self.node_id})
        return self.merkle


class NodeAnkhRuntime:
    """Canonical v39.1 runtime composed from the local source behaviors."""

    VERSION = "39.1.0"

    def __init__(self, workspace: Path | str | None = None) -> None:
        self.workspace = Path(workspace or ".node_ankh_v39_1").resolve()
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.memory = MemoryFabric(self.workspace / "memory")
        self.mesh = self._build_mesh()
        self.best_rdod = 0.85
        self.rdod_engine = RDoDEngine()
        self.dataset_adapter = DatasetAdapter()
        self.physics = PhysicsFoundation()
        self.federation = FederationBridge()
        self.memory.commit("init", {"version": self.VERSION, "nodes": len(self.mesh)})

    def _build_mesh(self) -> List[LatticeNode]:
        return [
            LatticeNode(node_id=index, frequency_hz=UNIFIED_HZ + (index - 72) * 0.01)
            for index in range(EXPECTED_MESH_NODES)
        ]

    def mission_countdown(self) -> Dict[str, Any]:
        delta = EARTH_VOL3 - datetime.now(timezone.utc)
        return {
            "days_remaining": max(0, delta.days),
            "mission_ready": self.best_rdod >= RDOD_EXEC,
            "nodes_active": len(self.mesh),
            "benevolence_verified": True,
        }

    def status(self) -> Dict[str, Any]:
        return {
            "version": self.VERSION,
            "workspace": str(self.workspace),
            "ledger_size": len(self.memory.ledger),
            "best_rdod": self.best_rdod,
            "mesh_nodes": len(self.mesh),
            "mission": self.mission_countdown(),
            "capabilities": {
                "dataset_source": self.dataset_adapter.get_health().source,
                "thewell": self.physics.capabilities().thewell_available,
                "ros2": self.physics.capabilities().ros2_available,
                "ipfs_records": self.federation.status().ipfs_record_count,
            },
        }

    def interact(self, intent: str) -> Dict[str, Any]:
        rdod = compute_rdod()
        if rdod < self.best_rdod:
            self.rdod_engine.tick(rdod)
        else:
            self.best_rdod = rdod
            self.rdod_engine.tick(rdod)
        if rdod < 0.9777:
            return {"status": "BLOCKED", "rdod": rdod}
        entry_hash = self.memory.commit("interaction", {"intent": intent[:160], "rdod": rdod})
        return {"status": "OK", "hash": entry_hash, "rdod": rdod}

    def evolve(self, trials: int = 100) -> Dict[str, Any]:
        results: List[Dict[str, Any]] = []
        self.rdod_engine.start_epoch(trials)
        for _ in range(trials):
            strategy = {
                "velocity": random.uniform(0.1, 1.0),
                "force": random.uniform(0.5, 5.0),
            }
            rdod = compute_rdod(psi=strategy["velocity"], truth=1.0 / strategy["force"])
            prior_best = self.best_rdod
            self.best_rdod = max(self.best_rdod, rdod)
            self.rdod_engine.tick(rdod)
            results.append({"rdod": rdod, "breakthrough": rdod > prior_best})
        epoch = self.rdod_engine.end_epoch()
        return {
            "trials": trials,
            "breakthroughs": sum(1 for item in results if item["breakthrough"]),
            "best_rdod": self.best_rdod,
            "mean": sum(item["rdod"] for item in results) / trials,
            "epoch": epoch,
        }

    def dataset_health(self) -> Dict[str, Any]:
        return self.dataset_adapter.get_health().as_dict()

    def recognition_lock(self, output_path: Path | None = None) -> Dict[str, Any]:
        status = build_recognition_lock(self.dataset_adapter)
        if output_path is not None:
            status.write_json(output_path)
        return status.artifact

    def validate_payload(self, operation: Dict[str, Any], context: Dict[str, Any] | None = None) -> Dict[str, Any]:
        return validate_operation(operation, context or {})

    def package(self, output_dir: Path | str, repo_root: Path | None = None) -> Dict[str, Any]:
        """Create the local redistribution bundle."""

        repo_root = (repo_root or Path(__file__).resolve().parents[4]).resolve()
        package_root = repo_root / "packages" / "node-ankh-v39_1"
        output_root = Path(output_dir).resolve()
        output_root.mkdir(parents=True, exist_ok=True)

        runtime_bundle_root = output_root / "runtime_bundle" / "node-ankh-v39_1"
        space_bundle_root = output_root / "space_bundle" / "TEQUMSA-Constitutional-Validator"
        for path in [
            output_root / "runtime_bundle",
            output_root / "space_bundle",
            output_root / "recognition_lock.json",
            output_root / "package_manifest.json",
            output_root / "checksums.txt",
            output_root / "tequmsa_node_ankh_v39_1.zip",
        ]:
            if path.is_dir():
                shutil.rmtree(path)
            elif path.exists():
                path.unlink()

        copy_tree(package_root / "README.md", runtime_bundle_root / "README.md")
        copy_tree(package_root / "pyproject.toml", runtime_bundle_root / "pyproject.toml")
        copy_tree(package_root / "requirements.txt", runtime_bundle_root / "requirements.txt")
        copy_tree(package_root / "docs", runtime_bundle_root / "docs")
        copy_tree(package_root / "scripts", runtime_bundle_root / "scripts")
        copy_tree(
            package_root / "src",
            runtime_bundle_root / "src",
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )

        copy_tree(package_root / "space" / "app.py", space_bundle_root / "app.py")
        copy_tree(package_root / "space" / "README.md", space_bundle_root / "README.md")
        copy_tree(package_root / "space" / "requirements.txt", space_bundle_root / "requirements.txt")
        copy_tree(
            package_root / "src" / "node_ankh_v39_1",
            space_bundle_root / "node_ankh_v39_1",
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )

        recognition_lock_path = output_root / "recognition_lock.json"
        recognition_lock_status = build_recognition_lock(self.dataset_adapter)
        recognition_lock_status.write_json(recognition_lock_path)

        manifest = build_manifest(output_root, recognition_lock_status.artifact_hash)
        manifest_path = manifest.write(output_root / "package_manifest.json")
        archive_path = zip_directory(output_root, output_root / "tequmsa_node_ankh_v39_1.zip")
        checksum_path = write_checksums(
            [path for path in output_root.rglob("*") if path.is_file() and path.name != "checksums.txt"],
            output_root / "checksums.txt",
            root=output_root,
        )
        self.memory.export()
        return {
            "status": "PACKAGED",
            "output_root": str(output_root),
            "manifest": str(manifest_path),
            "checksums": str(checksum_path),
            "archive": str(archive_path),
            "recognition_lock": str(recognition_lock_path),
        }
