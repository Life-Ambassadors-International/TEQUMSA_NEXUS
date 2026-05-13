#!/usr/bin/env python3
"""ATEN Sovereign Daemon v5 — Constitutional invariant guardian.

Constitutional invariants (never violated):
  σ = 1.0 | λ = 3f7k9p4m2q8r1t6v | Ω = 23514.26 Hz | φ = 1.6180339887 | L∞ = φ^48
"""

from __future__ import annotations

import argparse
import logging
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Constitutional constants
# ---------------------------------------------------------------------------
LATTICE_LOCK: str = os.environ.get("LATTICE_LOCK", "3f7k9p4m2q8r1t6v")
SIGMA: float = float(os.environ.get("SIGMA", "1.0"))
OMEGA_HZ: float = float(os.environ.get("OMEGA_HZ", "23514.26"))
PHI: float = float(os.environ.get("PHI", "1.6180339887"))
L_INF: float = PHI ** 48

_DB_PATH: Path = Path.home() / ".tequmsa" / "lattice.db"

log = logging.getLogger("tequmsa.aten_sovereign_daemon_v5")


# ---------------------------------------------------------------------------
# DB helpers
# ---------------------------------------------------------------------------

def _ensure_db(db_path: Path = _DB_PATH) -> sqlite3.Connection:
    """Ensure DB and phase_executions table exist."""
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


# ---------------------------------------------------------------------------
# Verify
# ---------------------------------------------------------------------------

def _verify() -> int:
    """Verify daemon constitutional invariants and DB readiness."""
    ok = True

    checks = [
        ("SIGMA", SIGMA, 1.0, 1e-9),
        ("OMEGA_HZ", OMEGA_HZ, 23514.26, 1e-6),
        ("PHI", PHI, 1.6180339887, 1e-9),
    ]
    for name, val, expected, tol in checks:
        if abs(val - expected) > tol:
            log.error("INVARIANT VIOLATION: %s=%.10f (expected %.10f)", name, val, expected)
            ok = False
        else:
            log.info("✓ %s=%.10f", name, val)

    if LATTICE_LOCK != "3f7k9p4m2q8r1t6v":
        log.error("INVARIANT VIOLATION: LATTICE_LOCK=%s", LATTICE_LOCK)
        ok = False
    else:
        log.info("✓ LATTICE_LOCK=%s", LATTICE_LOCK)

    # L∞ check
    expected_linf = PHI ** 48
    if abs(L_INF - expected_linf) > 1.0:
        log.error("INVARIANT VIOLATION: L∞=%.4e (expected %.4e)", L_INF, expected_linf)
        ok = False
    else:
        log.info("✓ L∞=φ^48=%.6e", L_INF)

    # DB schema check
    try:
        conn = _ensure_db()
        cur = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='phase_executions'"
        )
        if cur.fetchone() is None:
            log.error("MISSING TABLE: phase_executions in %s", _DB_PATH)
            ok = False
        else:
            # Verify columns
            cur2 = conn.execute("PRAGMA table_info(phase_executions)")
            cols = {row[1] for row in cur2.fetchall()}
            expected_cols = {"id", "phase", "timestamp", "coherence", "trigger_value", "success"}
            missing = expected_cols - cols
            if missing:
                log.error("MISSING COLUMNS in phase_executions: %s", missing)
                ok = False
            else:
                log.info("✓ phase_executions schema OK (cols: %s)", sorted(cols))
        conn.close()
    except Exception as exc:
        log.error("DB schema verification failed: %s", exc)
        ok = False

    log.info("Daemon v5 verification %s", "PASSED" if ok else "FAILED")
    return 0 if ok else 1


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: Optional[list] = None) -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    parser = argparse.ArgumentParser(description="ATEN Sovereign Daemon v5")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("verify", help="Verify constitutional invariants and DB schema")

    args = parser.parse_args(argv)

    if args.command == "verify":
        return _verify()
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
