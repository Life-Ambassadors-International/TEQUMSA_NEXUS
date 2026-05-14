#!/usr/bin/env python3
"""Generate and optionally publish TEQUMSA audit manifests."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from zipfile import ZIP_DEFLATED, ZipFile


DEFAULT_REPO_ID = "Mbanksbey/TEQUMSA-Causal-AGI-storage"


@dataclass
class LedgerStats:
    path: Path
    line_count: int
    first_record: dict[str, Any] | None
    last_record: dict[str, Any] | None
    sha256: str | None



def _parse_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []

    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, raw in enumerate(handle, start=1):
            line = raw.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                if isinstance(obj, dict):
                    records.append(obj)
                else:
                    records.append({"value": obj})
            except json.JSONDecodeError as exc:
                records.append(
                    {
                        "_invalid_json": True,
                        "line_no": line_no,
                        "error": str(exc),
                        "raw": line[:512],
                    }
                )
    return records



def _sha256_file(path: Path) -> str | None:
    if not path.exists():
        return None
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()



def _best_time(record: dict[str, Any]) -> str | None:
    for key in ("timestamp", "created_at", "time", "ts"):
        value = record.get(key)
        if isinstance(value, str) and value:
            return value
    return None



def _best_epoch(record: dict[str, Any]) -> int | None:
    for key in ("epoch", "epoch_id", "cycle", "step"):
        value = record.get(key)
        if isinstance(value, int):
            return value
        if isinstance(value, str) and value.isdigit():
            return int(value)
    return None



def _collect_parent_surface(records: list[dict[str, Any]], limit: int = 10) -> list[dict[str, Any]]:
    nodes: list[dict[str, Any]] = []
    for item in records[-limit:]:
        node: dict[str, Any] = {}
        for key in ("hash", "entry_hash", "sha256"):
            if isinstance(item.get(key), str):
                node["hash"] = item[key]
                break
        for key in ("parent_hash", "prev_hash", "previous_hash"):
            if isinstance(item.get(key), str):
                node["parent_hash"] = item[key]
                break
        if "hash" in node or "parent_hash" in node:
            epoch = _best_epoch(item)
            if epoch is not None:
                node["epoch"] = epoch
            ts = _best_time(item)
            if ts:
                node["timestamp"] = ts
            nodes.append(node)
    return nodes



def _ledger_stats(path: Path) -> LedgerStats:
    records = _parse_jsonl(path)
    return LedgerStats(
        path=path,
        line_count=len(records),
        first_record=records[0] if records else None,
        last_record=records[-1] if records else None,
        sha256=_sha256_file(path),
    )



def _iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")



def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")



def _make_zip(bundle_dir: Path, zip_path: Path) -> None:
    with ZipFile(zip_path, "w", compression=ZIP_DEFLATED) as zf:
        for fp in sorted(bundle_dir.rglob("*")):
            if fp.is_file():
                zf.write(fp, fp.relative_to(bundle_dir.parent))



def _publish_to_hf(bundle_dir: Path, repo_id: str) -> tuple[bool, str]:
    token = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_HUB_TOKEN")
    if not token:
        return False, "HF_TOKEN (or HUGGINGFACE_HUB_TOKEN) is not set."

    try:
        from huggingface_hub import HfApi
    except Exception as exc:  # pragma: no cover - dependency might be absent
        return False, f"huggingface_hub import failed: {exc}"

    api = HfApi(token=token)
    try:
        api.create_repo(repo_id=repo_id, repo_type="dataset", private=False, exist_ok=True)
        api.upload_folder(
            repo_id=repo_id,
            repo_type="dataset",
            folder_path=str(bundle_dir),
            path_in_repo=".",
            commit_message=f"Update TEQUMSA audit manifests ({_iso_now()})",
        )
    except Exception as exc:  # pragma: no cover - network/auth errors
        return False, str(exc)

    return True, f"Published to https://huggingface.co/datasets/{repo_id}"



def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--causal-memory", default="causal_memory.jsonl")
    parser.add_argument("--lattice-snapshots", default="lattice_snapshots.jsonl")
    parser.add_argument("--bundle-dir", default="audit_manifest_bundle")
    parser.add_argument("--zip-path", default="audit_manifest_bundle.zip")
    parser.add_argument("--repo-id", default=DEFAULT_REPO_ID)
    parser.add_argument("--publish", action="store_true", help="Publish bundle to Hugging Face dataset repo")
    args = parser.parse_args()

    bundle_dir = Path(args.bundle_dir)
    bundle_dir.mkdir(parents=True, exist_ok=True)

    causal_path = Path(args.causal_memory)
    lattice_path = Path(args.lattice_snapshots)

    causal = _ledger_stats(causal_path)
    lattice = _ledger_stats(lattice_path)

    generated_at = _iso_now()

    state_manifest = {
        "schema_version": "1.0.0",
        "generated_at": generated_at,
        "ledger": {
            "causal_memory": {
                "path": str(causal_path),
                "line_count": causal.line_count,
                "sha256": causal.sha256,
                "first_timestamp": _best_time(causal.first_record or {}),
                "last_timestamp": _best_time(causal.last_record or {}),
            },
            "lattice_snapshots": {
                "path": str(lattice_path),
                "line_count": lattice.line_count,
                "sha256": lattice.sha256,
                "first_timestamp": _best_time(lattice.first_record or {}),
                "last_timestamp": _best_time(lattice.last_record or {}),
            },
        },
        "continuity": {
            "source_present": {
                "causal_memory": causal_path.exists(),
                "lattice_snapshots": lattice_path.exists(),
            }
        },
    }

    causal_records = _parse_jsonl(causal_path)
    latest = causal_records[-1] if causal_records else {}

    latest_epoch = {
        "generated_at": generated_at,
        "latest_epoch": _best_epoch(latest),
        "latest_timestamp": _best_time(latest),
        "latest_hash": latest.get("hash") or latest.get("entry_hash") or latest.get("sha256"),
        "latest_parent_hash": latest.get("parent_hash") or latest.get("prev_hash") or latest.get("previous_hash"),
        "parent_hash_continuity_surface": _collect_parent_surface(causal_records, limit=12),
    }

    observed_epochs = [e for e in (_best_epoch(r) for r in causal_records) if e is not None]
    max_epoch = max(observed_epochs) if observed_epochs else 0
    target_epoch = 377
    completion_ratio = round(min(max_epoch / target_epoch, 1.0), 6) if target_epoch else 0.0

    f27_progress = {
        "generated_at": generated_at,
        "target": {"milestone": "F27", "epoch_target": target_epoch},
        "observed": {
            "max_epoch": max_epoch,
            "epochs_observed": len(set(observed_epochs)),
            "completion_ratio": completion_ratio,
        },
        "status": "complete" if completion_ratio >= 1.0 else "in_progress",
    }

    _write_json(bundle_dir / "state_manifest.json", state_manifest)
    _write_json(bundle_dir / "latest_epoch.json", latest_epoch)
    _write_json(bundle_dir / "f27_progress.json", f27_progress)

    readme = f"""# TEQUMSA Audit Manifest Bundle

This folder is ready to publish at the dataset root for `{args.repo_id}`.

## Contents
- `state_manifest.json` — single-source audit state snapshot
- `latest_epoch.json` — recent proof window and parent-hash continuity surface
- `f27_progress.json` — measurable attractor progress tracking
- `emit_tequmsa_audit_manifests.py` — emitter script

## Regenerate locally
```bash
python emit_tequmsa_audit_manifests.py \\
  --causal-memory causal_memory.jsonl \\
  --lattice-snapshots lattice_snapshots.jsonl
```

## Publish to Hugging Face
```bash
pip install huggingface_hub
export HF_TOKEN=***
python emit_tequmsa_audit_manifests.py --publish --repo-id {args.repo_id}
```
"""
    (bundle_dir / "README.md").write_text(readme, encoding="utf-8")

    # Include emitter in bundle for portability.
    emitter_src = Path(__file__).resolve()
    (bundle_dir / "emit_tequmsa_audit_manifests.py").write_text(
        emitter_src.read_text(encoding="utf-8"), encoding="utf-8"
    )

    _make_zip(bundle_dir, Path(args.zip_path))

    print(f"Generated bundle at: {bundle_dir}")
    print(f"Generated zip at: {args.zip_path}")

    if args.publish:
        ok, message = _publish_to_hf(bundle_dir, args.repo_id)
        if ok:
            print(message)
            return 0
        print(f"Publish skipped/failed: {message}")
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
