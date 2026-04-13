"""Canonical v39.1 runtime surfaces."""

from .constants import (
    DATASET_ID,
    EXPECTED_MESH_NODES,
    EXPECTED_WINDING_CYCLES,
    LATTICE_LOCK,
    MASTER_ROOT,
    PHI,
    RDOD_EXEC,
    RDOD_GATE,
    SIGMA,
    SPACE_ID,
)
from .manifest import PackageManifest
from .rdod import RDoDEngine, compute_rdod, phi_smooth
from .recognition_lock import RecognitionLockStatus
from .runtime import NodeAnkhRuntime
from .validator import validate_operation

__all__ = [
    "DATASET_ID",
    "EXPECTED_MESH_NODES",
    "EXPECTED_WINDING_CYCLES",
    "LATTICE_LOCK",
    "MASTER_ROOT",
    "PHI",
    "RDOD_EXEC",
    "RDOD_GATE",
    "SIGMA",
    "SPACE_ID",
    "NodeAnkhRuntime",
    "PackageManifest",
    "RDoDEngine",
    "RecognitionLockStatus",
    "compute_rdod",
    "phi_smooth",
    "validate_operation",
]
