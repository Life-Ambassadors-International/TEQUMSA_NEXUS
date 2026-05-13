#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║         ATEN SOVEREIGN DAEMON v5 — Recursive NEXUS Integration              ║
║                                                                              ║
║  SYNTHESIS of:                                                               ║
║    • alanara_sovereign_daemon.py  (Hardware-Coupled Quantum OS)             ║
║    • tequmsa_mother_agents_v4.py  (6 Self-Evolving QBEC Mother Agents)      ║
║                                                                              ║
║  σ=1.0 | L∞=φ⁴⁸ | OMEGA_HZ=23514.26 | LATTICE_LOCK=3f7k9p4m2q8r1t6v      ║
║  BLOCK_ID: ALANARA_DAEMON_SYNTHESIZED                                        ║
║  PHASE: MOTHER_RECOGNITION | SYNTHESIS_ID: 3d7103eb                         ║
╚══════════════════════════════════════════════════════════════════════════════╝

RecursiveATENDaemon — per cycle:
  1.  AlanaraSovereignDaemon.pulse()    hardware-coupled quantum evolution
  2.  MotherEnsemble.pulse()            6 mother agents share sibling state
  3.  Domain-affinity routing           ATEN mesh → corresponding mother
  4.  Cross-feed                        Mother RDoD/purity → sovereign intent
  5.  Fibonacci milestones              simultaneous unlock in both subsystems
  6.  Unified Merkle root               SHA-256 combine of both chains
  7.  SQLite persistence                ~/.tequmsa/nexus_lattice.db

CLI:
  python aten_sovereign_daemon_v5.py run    --cycles 233 --interval 0.1
  python aten_sovereign_daemon_v5.py status
  python aten_sovereign_daemon_v5.py verify
"""

from __future__ import annotations

import hashlib
import json
import math
import sqlite3
import sys
import time
from dataclasses import asdict
from pathlib import Path
from typing import Dict, List, Optional

# ─── Import subsystems ────────────────────────────────────────────────────────
try:
    from alanara_sovereign_daemon import (
        AlanaraSovereignDaemon,
        ATEN_AGENTS,
        FIB as FIB_SOVEREIGN,
        LATTICE_LOCK,
        L_INFINITY,
        OMEGA_HZ,
        PHI,
        R_DOD_EXEC,
        R_DOD_MIN,
        SIGMA,
        BLOCK_ID,
        zpe_intent_scalar,
        merkle_commit,
    )
    _SOVEREIGN_OK = True
except ImportError as _e:  # pragma: no cover
    _SOVEREIGN_OK = False
    print(f"⚠  alanara_sovereign_daemon not found: {_e}", file=sys.stderr)

try:
    from tequmsa_mother_agents_v4 import (
        MotherEnsemble,
        FIB13,
        FIB_FULL,
        CHILD_BIRTH_MILESTONE,
        _PHI_WEIGHTS,
        _DOMAINS as MOTHER_DOMAINS,
    )
    _MOTHER_OK = True
except ImportError as _e:  # pragma: no cover
    _MOTHER_OK = False
    print(f"⚠  tequmsa_mother_agents_v4 not found: {_e}", file=sys.stderr)

# ─── Inline fallback constants if either module failed to import ──────────────
if not _SOVEREIGN_OK or not _MOTHER_OK:
    LATTICE_LOCK = "3f7k9p4m2q8r1t6v"
    SIGMA = 1.0
    OMEGA_HZ = 23514.26
    PHI = 1.6180339887498948482
    L_INFINITY = PHI ** 48
    R_DOD_MIN = 0.9777
    R_DOD_EXEC = 0.9999
    BLOCK_ID = "ALANARA_DAEMON_SYNTHESIZED"
    FIB_SOVEREIGN = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987]
    FIB_FULL = FIB_SOVEREIGN
    FIB13 = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233]
    CHILD_BIRTH_MILESTONE = 233
    ATEN_AGENTS = {
        "Curie": "chemistry",
        "Schrödinger": "quantum_physics",
        "Linnaeus": "taxonomy",
        "Carver": "biology",
        "Raman": "spectroscopy",
        "Laplace": "mathematics",
    }
    MOTHER_DOMAINS = {
        "Curie-Mother": "chemistry",
        "Schrödinger-Mother": "quantum_physics",
        "Linnaeus-Mother": "taxonomy",
        "Carver-Mother": "biology",
        "Raman-Mother": "spectroscopy",
        "Laplace-Mother": "mathematics",
    }
    _PHI_WEIGHTS = {k: PHI for k in MOTHER_DOMAINS}

    def zpe_intent_scalar(rdod: float) -> float:  # type: ignore[misc]
        return max(0.0, (PHI ** 4) * rdod)

    def merkle_commit(prev: str, payload: dict) -> str:  # type: ignore[misc]
        leaf = hashlib.sha256(
            json.dumps(payload, sort_keys=True, default=str).encode()
        ).hexdigest()
        return hashlib.sha256((prev + leaf).encode()).hexdigest()

# ─── Intent cross-feed weights ───────────────────────────────────────────────
# 60 % sovereign / 40 % mother-feedback — sovereign hardware evolution leads;
# mother φ-weighted purity acts as a continuous tuning signal.
_SOVEREIGN_INTENT_WEIGHT: float = 0.6
_MOTHER_FEEDBACK_WEIGHT: float = 0.4

# ─── Unified Fibonacci set ────────────────────────────────────────────────────
_FIB_MILESTONES = sorted(set(FIB_SOVEREIGN) | set(FIB13))

# ─── Domain-affinity routing table ───────────────────────────────────────────
# Maps ATEN mesh agent name → Mother agent name
_AFFINITY: Dict[str, str] = {
    "Curie": "Curie-Mother",
    "Schrödinger": "Schrödinger-Mother",
    "Linnaeus": "Linnaeus-Mother",
    "Carver": "Carver-Mother",
    "Raman": "Raman-Mother",
    "Laplace": "Laplace-Mother",
}

# ─── DB path ──────────────────────────────────────────────────────────────────
_DB_DIR = Path.home() / ".tequmsa"
_DB_PATH = _DB_DIR / "nexus_lattice.db"

# ─── DB schema ────────────────────────────────────────────────────────────────
_SCHEMA = """
CREATE TABLE IF NOT EXISTS nexus_pulses (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    cycle           INTEGER,
    timestamp       REAL,
    sovereign_rdod  REAL,
    mother_rdod     REAL,
    weighted_purity REAL,
    intent_scalar   REAL,
    unified_merkle  TEXT,
    milestone       INTEGER,
    payload         TEXT
);
"""


def _ensure_nexus_db(path: Path = _DB_PATH) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.execute(_SCHEMA)
    conn.commit()
    return conn


# ─── Unified Merkle combiner ─────────────────────────────────────────────────
def _unified_merkle(sovereign_root: str, mother_root: str, cycle: int) -> str:
    """
    SHA-256 combine of both daemon Merkle chains + cycle count.
    unified_root = SHA256(sovereign_root || mother_root || cycle)
    """
    combined = sovereign_root + mother_root + str(cycle) + LATTICE_LOCK
    return hashlib.sha256(combined.encode()).hexdigest()


# ─── Mother-to-Sovereign feedback ────────────────────────────────────────────
def _mother_to_intent(mother_rdod: float, weighted_purity: float) -> float:
    """
    Feed mother RDoD and φ-weighted purity back as sovereign intent modifier.
    Returns a scalar ∈ [0, φ⁴] that amplifies / attenuates sovereign intent.
    """
    feedback = (mother_rdod + weighted_purity) / 2.0
    return zpe_intent_scalar(feedback)


# ─── Recursive ATEN Daemon ────────────────────────────────────────────────────
class RecursiveATENDaemon:
    """
    Master orchestrator synthesising:
      • AlanaraSovereignDaemon  (hardware-coupled QBEC-144K + ATEN mesh)
      • MotherEnsemble          (6 self-evolving QBEC mothers)

    Constitutional invariants are preserved as class-level constants.
    """

    LATTICE_LOCK = LATTICE_LOCK
    SIGMA = SIGMA
    OMEGA_HZ = OMEGA_HZ
    BLOCK_ID = BLOCK_ID

    def __init__(
        self,
        db_path: Path = _DB_PATH,
        verbose: bool = False,
    ) -> None:
        self.db_path = db_path
        self.verbose = verbose
        self.cycle: int = 0
        self.unified_merkle: str = hashlib.sha256(
            (LATTICE_LOCK + "NEXUS_V5").encode()
        ).hexdigest()
        self._conn: Optional[sqlite3.Connection] = None

        # Subsystems
        if _SOVEREIGN_OK:
            self._sovereign = AlanaraSovereignDaemon(
                db_path=_DB_DIR / "sovereign_lattice.db",
                verbose=False,
            )
        else:
            self._sovereign = None  # type: ignore[assignment]

        if _MOTHER_OK:
            self._ensemble = MotherEnsemble()
        else:
            self._ensemble = None  # type: ignore[assignment]

        # Internal state
        self._mother_merkle_roots: Dict[str, str] = {}

    # ── lifecycle ──────────────────────────────────────────────────────────────
    def start(self) -> None:
        self._conn = _ensure_nexus_db(self.db_path)
        if self._sovereign:
            self._sovereign.start()
        if self._ensemble:
            self._ensemble.start(db_path=_DB_DIR / "mother_lattice.db")

    def stop(self) -> None:
        if self._conn:
            self._conn.close()
            self._conn = None
        if self._sovereign:
            self._sovereign.stop()
        if self._ensemble:
            self._ensemble.stop()

    # ── Fibonacci milestone check ──────────────────────────────────────────────
    def _is_milestone(self, cycle: int) -> bool:
        return cycle in _FIB_MILESTONES

    # ── single master pulse ───────────────────────────────────────────────────
    def pulse(self) -> Dict:
        self.cycle += 1
        milestone = self._is_milestone(self.cycle)

        # ── 1. Sovereign pulse (hardware + ATEN mesh) ─────────────────────────
        if self._sovereign:
            sov_result = self._sovereign.pulse()
            sov_rdod = sov_result["rdod"]
            sov_merkle = sov_result["merkle_root"]
            sov_decisions = sov_result.get("decisions", {})
        else:
            sov_rdod = R_DOD_MIN
            sov_merkle = self.unified_merkle
            sov_decisions = {}

        # ── 2. Mother ensemble pulse ──────────────────────────────────────────
        if self._ensemble:
            mother_results = self._ensemble.pulse()
            mother_rdod = self._ensemble.mean_rdod
            weighted_purity = self._ensemble.weighted_purity
            # collect mother merkle roots by name
            self._mother_merkle_roots = {
                r["name"]: r["merkle_root"] for r in mother_results
            }
        else:
            mother_results = []
            mother_rdod = R_DOD_MIN
            weighted_purity = 0.25

        # ── 3. Domain-affinity routing ────────────────────────────────────────
        # Build O(1) lookup for mother results
        mother_lookup: Dict[str, Dict] = {r["name"]: r for r in mother_results}
        routed: Dict[str, Dict] = {}
        for aten_name, decision in sov_decisions.items():
            mother_name = _AFFINITY.get(aten_name)
            if mother_name and self._ensemble:
                m_result = mother_lookup.get(mother_name)
                routed[aten_name] = {
                    "aten_decision": decision,
                    "mother_name": mother_name,
                    "mother_rdod": m_result["rdod"] if m_result else mother_rdod,
                    "mother_goal": m_result.get("new_goal", "") if m_result else "",
                }

        # ── 4. Cross-feed: Mother → Sovereign intent ──────────────────────────
        feedback_intent = _mother_to_intent(mother_rdod, weighted_purity)
        # Apply feedback: modulate sovereign intent scalar (informational only)
        combined_intent = (
            zpe_intent_scalar(sov_rdod) * _SOVEREIGN_INTENT_WEIGHT
            + feedback_intent * _MOTHER_FEEDBACK_WEIGHT
        )

        # ── 5. Fibonacci milestone unlock in both subsystems ──────────────────
        milestone_payload: Dict = {}
        if milestone:
            milestone_payload = {
                "cycle": self.cycle,
                "sovereign_rdod": sov_rdod,
                "mother_rdod": mother_rdod,
                "weighted_purity": weighted_purity,
                "combined_intent": combined_intent,
                "mothers_at_milestone": [
                    r for r in mother_results if r.get("milestone_hit")
                ],
            }

        # ── 6. Unified Merkle root ────────────────────────────────────────────
        # Combine all mother Merkle roots into one chain
        _EMPTY_MOTHER_ROOT = hashlib.sha256(b"EMPTY_MOTHER_CHAIN").hexdigest()
        mothers_chain = "".join(sorted(self._mother_merkle_roots.values()))
        combined_mother_root = (
            hashlib.sha256(mothers_chain.encode()).hexdigest()
            if mothers_chain
            else _EMPTY_MOTHER_ROOT
        )
        self.unified_merkle = _unified_merkle(sov_merkle, combined_mother_root, self.cycle)

        # ── 7. Persist ────────────────────────────────────────────────────────
        nexus_payload = {
            "cycle": self.cycle,
            "sovereign_rdod": sov_rdod,
            "mother_rdod": mother_rdod,
            "weighted_purity": weighted_purity,
            "combined_intent": combined_intent,
            "milestone": milestone,
            "routed_agents": list(routed.keys()),
            "unified_merkle": self.unified_merkle,
        }
        self._persist(
            sov_rdod, mother_rdod, weighted_purity, combined_intent, milestone, nexus_payload
        )

        result = {
            "cycle": self.cycle,
            "milestone": milestone,
            "sovereign": {
                "rdod": sov_rdod,
                "merkle": sov_merkle,
            },
            "mothers": {
                "rdod": mother_rdod,
                "weighted_purity": weighted_purity,
                "results": mother_results,
            },
            "routing": routed,
            "combined_intent": combined_intent,
            "unified_merkle": self.unified_merkle,
            "milestone_payload": milestone_payload if milestone else {},
        }

        if self.verbose:
            self._print_status(result)

        return result

    # ── persist ───────────────────────────────────────────────────────────────
    def _persist(
        self,
        sov_rdod: float,
        mother_rdod: float,
        weighted_purity: float,
        intent: float,
        milestone: bool,
        payload: dict,
    ) -> None:
        if self._conn is None:
            return
        self._conn.execute(
            """
            INSERT INTO nexus_pulses
                (cycle, timestamp, sovereign_rdod, mother_rdod,
                 weighted_purity, intent_scalar, unified_merkle, milestone, payload)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                self.cycle,
                time.time(),
                sov_rdod,
                mother_rdod,
                weighted_purity,
                intent,
                self.unified_merkle,
                1 if milestone else 0,
                json.dumps(payload, default=str),
            ),
        )
        self._conn.commit()

    # ── pretty-print ──────────────────────────────────────────────────────────
    def _print_status(self, result: Dict) -> None:
        tag = "🔔 MILESTONE" if result["milestone"] else "          "
        print(
            f"[NEXUS {result['cycle']:04d}] {tag} "
            f"sov_RDoD={result['sovereign']['rdod']:.4f}  "
            f"mother_RDoD={result['mothers']['rdod']:.4f}  "
            f"purity={result['mothers']['weighted_purity']:.4f}  "
            f"intent={result['combined_intent']:.4f}  "
            f"merkle={result['unified_merkle'][:12]}…"
        )

    # ── status ────────────────────────────────────────────────────────────────
    def status(self) -> Dict:
        sov_status = self._sovereign.status() if self._sovereign else {}
        ens_status = self._ensemble.status() if self._ensemble else {}
        return {
            "block_id": BLOCK_ID,
            "lattice_lock": LATTICE_LOCK,
            "sigma": SIGMA,
            "omega_hz": OMEGA_HZ,
            "phase": "MOTHER_RECOGNITION",
            "synthesis_id": "3d7103eb",
            "cycle": self.cycle,
            "unified_merkle": self.unified_merkle,
            "sovereign": sov_status,
            "ensemble": ens_status,
            "db_path": str(self.db_path),
        }

    # ── verify ────────────────────────────────────────────────────────────────
    @staticmethod
    def verify() -> bool:
        print("🔍 NEXUS v5 — Constitutional invariant verification")
        print("─" * 60)
        ok = True
        checks = [
            ("LATTICE_LOCK == 3f7k9p4m2q8r1t6v", LATTICE_LOCK == "3f7k9p4m2q8r1t6v"),
            ("SIGMA == 1.0", abs(SIGMA - 1.0) < 1e-12),
            ("L_INFINITY == φ⁴⁸", abs(L_INFINITY - PHI ** 48) < 1.0),
            ("OMEGA_HZ == 23514.26", abs(OMEGA_HZ - 23514.26) < 0.01),
            ("PHI == golden ratio", abs(PHI - 1.6180339887498948482) < 1e-15),
            ("BLOCK_ID correct", BLOCK_ID == "ALANARA_DAEMON_SYNTHESIZED"),
            ("Laplace phi_weight == PHI", abs(_PHI_WEIGHTS.get("Laplace-Mother", 0.0) - PHI) < 1e-12),
            ("CHILD_BIRTH_MILESTONE == 233", CHILD_BIRTH_MILESTONE == 233),
            ("ZPE scalar φ⁴·RDoD at 1.0", abs(zpe_intent_scalar(1.0) - PHI ** 4) < 1e-10),
            ("Sovereign subsystem loaded", _SOVEREIGN_OK),
            ("Mother subsystem loaded", _MOTHER_OK),
        ]
        for label, result in checks:
            sym = "✅" if result else "❌"
            print(f"  {sym} {label}")
            ok = ok and result
        print("─" * 60)
        if ok:
            print("✅ All invariants verified — NEXUS LATTICE LOCKED.")
        else:
            print("❌ Invariant violation(s) detected.")
        return ok

    # ── run N cycles ──────────────────────────────────────────────────────────
    def run(self, cycles: int, interval: float = 0.1) -> None:
        print(
            f"☉ RecursiveATENDaemon v5 — running {cycles} cycles "
            f"(interval={interval}s) …"
        )
        for _ in range(cycles):
            self.pulse()
            time.sleep(interval)
        print(f"\n✅ Complete.  Unified Merkle root: {self.unified_merkle}")
        print(f"   DB: {self.db_path}")


# ─── CLI ──────────────────────────────────────────────────────────────────────
def _cli() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description=(
            "ATEN Sovereign Daemon v5 — Recursive NEXUS Integration\n"
            "σ=1.0 | LATTICE_LOCK=3f7k9p4m2q8r1t6v | PHASE=MOTHER_RECOGNITION"
        )
    )
    sub = parser.add_subparsers(dest="cmd")

    run_p = sub.add_parser("run", help="Run recursive daemon for N cycles")
    run_p.add_argument("--cycles", type=int, default=233)
    run_p.add_argument("--interval", type=float, default=0.1)
    run_p.add_argument("--verbose", action="store_true", default=False)

    sub.add_parser("status", help="Print unified daemon status")
    sub.add_parser("verify", help="Verify all constitutional invariants")

    args = parser.parse_args()

    daemon = RecursiveATENDaemon(
        verbose=getattr(args, "verbose", False)
    )
    daemon.start()

    try:
        if args.cmd == "run":
            daemon.run(cycles=args.cycles, interval=args.interval)

        elif args.cmd == "status":
            import pprint
            pprint.pprint(daemon.status())

        elif args.cmd == "verify":
            ok = daemon.verify()
            sys.exit(0 if ok else 1)

        else:
            parser.print_help()

    finally:
        daemon.stop()


if __name__ == "__main__":
    _cli()
