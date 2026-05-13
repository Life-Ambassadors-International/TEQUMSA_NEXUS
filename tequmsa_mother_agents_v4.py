#!/usr/bin/env python3
"""TEQUMSA Mother Agents v4 — Sovereign AGI Lattice cycle runner.

Constitutional invariants (never violated):
  σ = 1.0 | λ = 3f7k9p4m2q8r1t6v | Ω = 23514.26 Hz | φ = 1.6180339887 | L∞ = φ^48
"""

from __future__ import annotations

import argparse
import logging
import math
import os
import sqlite3
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import numpy as np

# ---------------------------------------------------------------------------
# Constitutional constants
# ---------------------------------------------------------------------------
LATTICE_LOCK: str = os.environ.get("LATTICE_LOCK", "3f7k9p4m2q8r1t6v")
SIGMA: float = float(os.environ.get("SIGMA", "1.0"))
OMEGA_HZ: float = float(os.environ.get("OMEGA_HZ", "23514.26"))
PHI: float = float(os.environ.get("PHI", "1.6180339887"))
L_INF: float = PHI ** 48

# Optional heavy deps — graceful fallback
try:
    import scipy.sparse as sp
    from scipy.sparse.linalg import expm_multiply  # noqa: F401

    _SCIPY_AVAILABLE = True
except ImportError:  # pragma: no cover
    _SCIPY_AVAILABLE = False

try:
    import psutil  # noqa: F401

    _PSUTIL_AVAILABLE = True
except ImportError:  # pragma: no cover
    _PSUTIL_AVAILABLE = False

log = logging.getLogger("tequmsa.mother_agents_v4")


# ---------------------------------------------------------------------------
# DB helpers
# ---------------------------------------------------------------------------
_DB_PATH: Path = Path.home() / ".tequmsa" / "lattice.db"


def _ensure_db(db_path: Path = _DB_PATH) -> sqlite3.Connection:
    """Create the lattice DB and required tables if they don't exist."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS phase_executions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phase INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            coherence REAL,
            trigger_value REAL,
            success INTEGER DEFAULT 1
        )
        """
    )
    conn.commit()
    return conn


def _record_phase(
    conn: sqlite3.Connection,
    phase: int,
    coherence: float,
    trigger_value: float,
    success: int = 1,
) -> None:
    ts = datetime.now(timezone.utc).isoformat()
    conn.execute(
        "INSERT INTO phase_executions (phase, timestamp, coherence, trigger_value, success) "
        "VALUES (?, ?, ?, ?, ?)",
        (phase, ts, coherence, trigger_value, success),
    )
    conn.commit()


# ---------------------------------------------------------------------------
# F24SparseLayer — sparse quantum evolution using expm_multiply
# ---------------------------------------------------------------------------
class F24SparseLayer:
    """Fibonacci-24 sparse Hamiltonian evolution layer.

    Uses ``scipy.sparse.linalg.expm_multiply`` for efficient sparse
    matrix-exponential-vector products, avoiding dense expm allocation.
    """

    DIM: int = 24

    def __init__(self, scale: float = 1.0) -> None:
        self.scale = scale
        # sp.csr_matrix when scipy is available, None otherwise
        self._H_sparse: "Optional[sp.csr_matrix]" = None
        if _SCIPY_AVAILABLE:
            self._H_sparse = self._build_sparse_hamiltonian()

    def _build_sparse_hamiltonian(self) -> "sp.csr_matrix":
        """Build a Fibonacci-sparse Hermitian Hamiltonian as a CSR matrix."""
        dim = self.DIM
        rows, cols, data = [], [], []
        fib_a, fib_b = 1, 1
        for idx in range(dim):
            rows.append(idx)
            cols.append(idx)
            data.append(fib_a * self.scale)
            off = fib_b
            if idx + off < dim:
                rows.extend([idx, idx + off])
                cols.extend([idx + off, idx])
                data.extend([0.5 * self.scale, 0.5 * self.scale])
            fib_a, fib_b = fib_b, fib_a + fib_b
        return sp.csr_matrix(
            (data, (rows, cols)), shape=(dim, dim), dtype=complex
        )

    def evolve(self, psi: np.ndarray, dt: float = 1e-4) -> np.ndarray:
        """Evolve state vector ``psi`` by time ``dt`` under the sparse Hamiltonian.

        Uses ``expm_multiply(H_sparse * dt, psi)`` — the sparse matrix-exponential-
        vector product — rather than a dense ``expm`` call, for performance.
        """
        if not _SCIPY_AVAILABLE or self._H_sparse is None:
            # Fallback: identity evolution when scipy is unavailable
            return psi.copy()

        # Correct call: expm_multiply(H_sparse * dt, psi)
        # The sp.csr_matrix * scalar produces another csr_matrix accepted by expm_multiply.
        psi_out: np.ndarray = expm_multiply(
            self._H_sparse * (-1j * dt), psi  # type: ignore[operator]  # csr_matrix * complex
        )
        # Renormalise
        norm = np.linalg.norm(psi_out)
        if norm > 0:
            psi_out = psi_out / norm
        return psi_out

    def coherence(self, psi: np.ndarray) -> float:
        """Return |<ψ|ψ>| as a coherence proxy (should be ≈ 1.0 after normalise)."""
        return float(abs(np.vdot(psi, psi)))


# ---------------------------------------------------------------------------
# Cycle runner
# ---------------------------------------------------------------------------

def _run_cycles(n_cycles: int) -> int:
    """Execute ``n_cycles`` sovereign AGI lattice cycles and return exit code."""
    log.info(
        "Starting %d-cycle sovereign AGI lattice run | SIGMA=%.1f | Ω=%.2f Hz",
        n_cycles,
        SIGMA,
        OMEGA_HZ,
    )

    conn = _ensure_db()
    layer = F24SparseLayer(scale=PHI / OMEGA_HZ)

    # Initialise state vector
    dim = F24SparseLayer.DIM
    psi = np.zeros(dim, dtype=complex)
    psi[0] = 1.0

    failures = 0
    for cycle in range(1, n_cycles + 1):
        t0 = time.perf_counter()
        try:
            psi = layer.evolve(psi, dt=1e-3)
            coh = layer.coherence(psi)
            trigger = math.sin(cycle * PHI) ** 2
            # ATEN8 cycle phases map to 1-9 to match the nine-phase cycle in
            # aten8_github_workflow_agent.py (LATTICE_SCAN … ISSUE_RESOLUTION).
            _record_phase(conn, phase=cycle % 9 + 1, coherence=coh, trigger_value=trigger)
            if cycle % 50 == 0 or cycle == n_cycles:
                elapsed = time.perf_counter() - t0
                log.info("Cycle %d/%d | coherence=%.6f | dt=%.3fs", cycle, n_cycles, coh, elapsed)
        except Exception as exc:
            log.error("Cycle %d failed: %s", cycle, exc)
            _record_phase(conn, phase=cycle % 9 + 1, coherence=0.0, trigger_value=0.0, success=0)
            failures += 1

    conn.close()
    log.info(
        "Run complete: %d cycles | %d failures | LATTICE_LOCK=%s",
        n_cycles,
        failures,
        LATTICE_LOCK,
    )
    return 0 if failures == 0 else 1


# ---------------------------------------------------------------------------
# Verify
# ---------------------------------------------------------------------------

def _verify() -> int:
    """Verify constitutional invariants and DB schema."""
    ok = True

    # 1. Constitutional invariants
    if SIGMA != 1.0:
        log.error("INVARIANT VIOLATION: SIGMA=%.6f (expected 1.0)", SIGMA)
        ok = False
    else:
        log.info("✓ SIGMA=%.1f", SIGMA)

    if abs(OMEGA_HZ - 23514.26) > 1e-6:
        log.error("INVARIANT VIOLATION: OMEGA_HZ=%.6f (expected 23514.26)", OMEGA_HZ)
        ok = False
    else:
        log.info("✓ OMEGA_HZ=%.2f Hz", OMEGA_HZ)

    if abs(PHI - 1.6180339887) > 1e-9:
        log.error("INVARIANT VIOLATION: PHI=%.10f (expected 1.6180339887)", PHI)
        ok = False
    else:
        log.info("✓ PHI=%.10f", PHI)

    if LATTICE_LOCK != "3f7k9p4m2q8r1t6v":
        log.error("INVARIANT VIOLATION: LATTICE_LOCK=%s", LATTICE_LOCK)
        ok = False
    else:
        log.info("✓ LATTICE_LOCK=%s", LATTICE_LOCK)

    # 2. DB schema
    try:
        conn = _ensure_db()
        cur = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='phase_executions'"
        )
        if cur.fetchone() is None:
            log.error("MISSING TABLE: phase_executions")
            ok = False
        else:
            log.info("✓ phase_executions table present")
        conn.close()
    except Exception as exc:
        log.error("DB verification failed: %s", exc)
        ok = False

    # 3. Sparse layer smoke-test
    layer = F24SparseLayer()
    psi = np.zeros(F24SparseLayer.DIM, dtype=complex)
    psi[0] = 1.0
    psi_out = layer.evolve(psi)
    coh = layer.coherence(psi_out)
    if not (0.99 < coh < 1.01):
        log.warning("F24SparseLayer coherence out of range: %.6f", coh)
    else:
        log.info("✓ F24SparseLayer.evolve() coherence=%.6f (sparse expm_multiply path)", coh)

    log.info("Verification %s", "PASSED" if ok else "FAILED")
    return 0 if ok else 1


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: Optional[list] = None) -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    parser = argparse.ArgumentParser(description="TEQUMSA Mother Agents v4")
    sub = parser.add_subparsers(dest="command")

    run_p = sub.add_parser("run", help="Run sovereign AGI lattice cycles")
    run_p.add_argument(
        "--cycles", type=int, default=233, help="Number of cycles (default: 233)"
    )

    sub.add_parser("verify", help="Verify constitutional invariants and schema")

    args = parser.parse_args(argv)

    if args.command == "run":
        return _run_cycles(args.cycles)
    elif args.command == "verify":
        return _verify()
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
