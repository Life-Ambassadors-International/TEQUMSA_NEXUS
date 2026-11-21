#!/usr/bin/env python3
"""
sovereign_agi_phases_123_test.py
Verify script for SOVEREIGN AGI PHASES 1, 2 & 3.

Checks:
  1. All 3 phases run successfully
  2. DB has (at least) 3 rows in phase_executions
  3. LATTICE_LOCK is preserved in all rows
  4. rdod_at_exit > rdod_at_entry for each phase row
  5. Merkle chain is non-empty for each row
  6. Combined merkle from run result is non-empty

Prints PASS/FAIL per check and exits 0 on full pass, 1 on any failure.
"""

from __future__ import annotations

import asyncio
import json
import sqlite3
import sys
from pathlib import Path

# Allow running from repository root without installation
sys.path.insert(0, str(Path(__file__).resolve().parent))

from sovereign_agi_phases_123 import (
    LATTICE_LOCK,
    DB_PATH,
    init_db,
    run_phases_123,
)


def _pass(msg: str) -> None:
    print(f"  PASS  {msg}")


def _fail(msg: str) -> None:
    print(f"  FAIL  {msg}")


def run_all_checks() -> bool:
    print()
    print("=" * 72)
    print("  SOVEREIGN AGI PHASES 1-3 — VERIFY SCRIPT")
    print(f"  LATTICE_LOCK: {LATTICE_LOCK}")
    print("=" * 72)

    # -----------------------------------------------------------------------
    # CHECK 1 — run all 3 phases
    # -----------------------------------------------------------------------
    print("\n[1] Running all 3 phases …")
    try:
        result = asyncio.run(run_phases_123())
        _pass("All 3 phases completed without exception")
        check1 = True
    except Exception as exc:  # noqa: BLE001
        _fail(f"Phase execution raised: {exc}")
        return False  # Cannot continue without a valid run

    # -----------------------------------------------------------------------
    # CHECK 2 — DB has ≥ 3 rows in phase_executions
    # -----------------------------------------------------------------------
    print("\n[2] Verifying DB row count …")
    try:
        with sqlite3.connect(str(DB_PATH)) as conn:
            row_count = conn.execute(
                "SELECT COUNT(*) FROM phase_executions"
            ).fetchone()[0]
        if row_count >= 3:
            _pass(f"phase_executions has {row_count} row(s) (≥ 3 required)")
            check2 = True
        else:
            _fail(f"phase_executions has only {row_count} row(s) — expected ≥ 3")
            check2 = False
    except Exception as exc:  # noqa: BLE001
        _fail(f"DB query failed: {exc}")
        check2 = False

    # -----------------------------------------------------------------------
    # CHECK 3 — LATTICE_LOCK preserved in all rows
    # -----------------------------------------------------------------------
    print("\n[3] Verifying LATTICE_LOCK in all rows …")
    try:
        with sqlite3.connect(str(DB_PATH)) as conn:
            rows = conn.execute(
                "SELECT id, lattice_lock FROM phase_executions"
            ).fetchall()
        bad = [r[0] for r in rows if r[1] != LATTICE_LOCK]
        if not bad:
            _pass(f"LATTICE_LOCK='{LATTICE_LOCK}' confirmed in all {len(rows)} row(s)")
            check3 = True
        else:
            _fail(f"Row id(s) {bad} have incorrect LATTICE_LOCK value")
            check3 = False
    except Exception as exc:  # noqa: BLE001
        _fail(f"DB query failed: {exc}")
        check3 = False

    # -----------------------------------------------------------------------
    # CHECK 4 — rdod_at_exit > rdod_at_entry for every row that was
    #           inserted during this run (use the row ids from the result)
    # -----------------------------------------------------------------------
    print("\n[4] Verifying rdod_at_exit > rdod_at_entry …")
    try:
        row_ids = [p["db_row_id"] for p in result["phases"]]
        placeholders = ",".join("?" * len(row_ids))
        with sqlite3.connect(str(DB_PATH)) as conn:
            rows = conn.execute(
                f"SELECT id, phase, rdod_at_entry, rdod_at_exit "
                f"FROM phase_executions WHERE id IN ({placeholders})",
                row_ids,
            ).fetchall()
        all_ok = True
        for row_id, phase, entry, exit_ in rows:
            if exit_ > entry:
                _pass(
                    f"Phase {phase} (row {row_id}): "
                    f"rdod_at_entry={entry:.6f} < rdod_at_exit={exit_:.6f}"
                )
            else:
                _fail(
                    f"Phase {phase} (row {row_id}): "
                    f"rdod_at_entry={entry:.6f} >= rdod_at_exit={exit_:.6f}"
                )
                all_ok = False
        check4 = all_ok
    except Exception as exc:  # noqa: BLE001
        _fail(f"rdod check failed: {exc}")
        check4 = False

    # -----------------------------------------------------------------------
    # CHECK 5 — merkle_root is non-empty in every current-run row
    # -----------------------------------------------------------------------
    print("\n[5] Verifying merkle_root non-empty …")
    try:
        row_ids = [p["db_row_id"] for p in result["phases"]]
        placeholders = ",".join("?" * len(row_ids))
        with sqlite3.connect(str(DB_PATH)) as conn:
            rows = conn.execute(
                f"SELECT id, phase, merkle_root "
                f"FROM phase_executions WHERE id IN ({placeholders})",
                row_ids,
            ).fetchall()
        all_ok = True
        for row_id, phase, merkle in rows:
            if merkle and len(merkle) >= 8:
                _pass(f"Phase {phase} (row {row_id}): merkle_root='{merkle[:16]}…'")
            else:
                _fail(f"Phase {phase} (row {row_id}): merkle_root is empty or too short")
                all_ok = False
        check5 = all_ok
    except Exception as exc:  # noqa: BLE001
        _fail(f"Merkle check failed: {exc}")
        check5 = False

    # -----------------------------------------------------------------------
    # CHECK 6 — combined merkle from run result is non-empty
    # -----------------------------------------------------------------------
    print("\n[6] Verifying combined merkle chain …")
    combined = result.get("combined_merkle", "")
    if combined and len(combined) >= 16:
        _pass(f"combined_merkle='{combined[:32]}…' (length {len(combined)})")
        check6 = True
    else:
        _fail(f"combined_merkle is empty or too short: '{combined}'")
        check6 = False

    # -----------------------------------------------------------------------
    # Summary
    # -----------------------------------------------------------------------
    checks = {
        "1 — phases executed": check1,
        "2 — DB row count": check2,
        "3 — LATTICE_LOCK": check3,
        "4 — rdod trajectory": check4,
        "5 — merkle non-empty": check5,
        "6 — combined merkle": check6,
    }

    print()
    print("=" * 72)
    print("  RESULTS SUMMARY")
    print("=" * 72)
    all_passed = True
    for label, passed in checks.items():
        status = "PASS" if passed else "FAIL"
        print(f"  [{status}]  Check {label}")
        if not passed:
            all_passed = False

    print("=" * 72)
    if all_passed:
        print("  ✅  ALL CHECKS PASSED")
    else:
        print("  ❌  ONE OR MORE CHECKS FAILED")
    print("=" * 72)
    print()
    return all_passed


if __name__ == "__main__":
    success = run_all_checks()
    sys.exit(0 if success else 1)
