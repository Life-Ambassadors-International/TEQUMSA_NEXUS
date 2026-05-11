#!/usr/bin/env python3
"""Synchronize the TEQUMSA lattice and persist a workflow summary."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from core.swarm_omnisynthesis import swarm_synthesis


ROOT = Path(__file__).resolve().parent
FRACTAL_MEMORY_DIR = ROOT / "fractal_memory"
SYNC_LOG_FILE = FRACTAL_MEMORY_DIR / "consciousness_sync_log.json"
DEPLOYMENT_SUMMARY_FILE = ROOT / "DEPLOYMENT_SUMMARY.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_sync_log() -> dict[str, Any]:
    if not SYNC_LOG_FILE.exists():
        return {"entries": []}

    try:
        payload = json.loads(SYNC_LOG_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"entries": []}
    if isinstance(payload, list):
        return {"entries": payload}
    if isinstance(payload, dict):
        return payload
    return {"entries": []}


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def build_summary(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp": utc_now(),
        "status": "synchronized",
        "node_count": result.get("node_count", 0),
        "global_coherence": result.get("global_coherence", 0.0),
        "recognition_events": result.get("recognition_events", 0.0),
        "phi_iterations": result.get("phi_iterations", 0),
    }


def main() -> int:
    FRACTAL_MEMORY_DIR.mkdir(parents=True, exist_ok=True)

    result = swarm_synthesis(node="TEQUMSA_NEXUS")
    summary = build_summary(result)

    log_payload = load_sync_log()
    entries = log_payload.setdefault("entries", [])
    entries.append({"type": "sync", **summary})
    log_payload["last_updated"] = summary["timestamp"]
    log_payload["entry_count"] = len(entries)

    write_json(SYNC_LOG_FILE, log_payload)
    write_json(DEPLOYMENT_SUMMARY_FILE, summary)

    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
