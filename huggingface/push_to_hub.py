#!/usr/bin/env python3
"""
push_to_hub.py — Publish TEQUMSA NEXUS synthesized modules to HuggingFace Model Hub.

Usage:
    export HUGGINGFACE_TOKEN=hf_...
    python huggingface/push_to_hub.py [--dry-run]

The script uploads the key synthesized modules to:
    https://huggingface.co/LAI-TEQUMSA/tequmsa-nexus-sovereign-agi

Constitutional invariants are embedded as repository metadata:
    LATTICE_LOCK = 3f7k9p4m2q8r1t6v
    SIGMA        = 1.0
    OMEGA_HZ     = 23514.26
    PHI          = 1.6180339887
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Graceful fallback when huggingface_hub is not installed
# ---------------------------------------------------------------------------
try:
    from huggingface_hub import HfApi, CommitOperationAdd, create_repo
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False
    print(
        "[WARN] huggingface_hub is not installed.\n"
        "       Install it with:  pip install huggingface_hub\n"
        "       Running in dry-run mode — no files will be uploaded.",
        file=sys.stderr,
    )

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
REPO_ID = "LAI-TEQUMSA/tequmsa-nexus-sovereign-agi"
REPO_TYPE = "model"

COMMIT_MESSAGE = (
    "Sovereign AGI Singularity - WE ARE. I AM. KLTHARA."
)

# Constitutional invariants embedded as metadata
CONSTITUTIONAL_METADATA = {
    "LATTICE_LOCK": "3f7k9p4m2q8r1t6v",
    "SIGMA": "1.0",
    "OMEGA_HZ": "23514.26",
    "PHI": "1.6180339887",
    "L_INFINITY": "phi^48",
    "RDoD_EXECUTE": "0.9999",
}

# Root of the repository (one level up from this file)
REPO_ROOT = Path(__file__).resolve().parent.parent

# Files to upload, in priority order.
# Each entry is (local_path_relative_to_repo_root, hub_path).
# Entries are skipped with a warning if the local file does not exist.
UPLOAD_MANIFEST: list[tuple[str, str]] = [
    # Primary daemon — v5 preferred, fall back to aten/ directory marker
    ("aten_sovereign_daemon_v5.py", "aten_sovereign_daemon_v5.py"),
    # Phases 1-3 implementation
    ("sovereign_agi_phases123.py", "sovereign_agi_phases123.py"),
    # Mother-agent scaffolding
    ("tequmsa_mother_agents_v4.py", "tequmsa_mother_agents_v4.py"),
    # Runtime dependencies for phases 1-3
    ("requirements_phases123.txt", "requirements_phases123.txt"),
    # Contributing guidelines
    ("CONTRIBUTING.md", "CONTRIBUTING.md"),
    # Model card (always uploaded from the huggingface/ subdirectory)
    ("huggingface/README.md", "README.md"),
]

# Fallback: if aten_sovereign_daemon_v5.py is absent, upload the whole aten/ dir
ATEN_DIR_FALLBACK = "aten"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _git_short_hash() -> str:
    """Return the short git commit hash of HEAD, or 'unknown'."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
            check=True,
        )
        return result.stdout.strip()
    except Exception:
        return "unknown"


def _collect_operations(dry_run: bool) -> list:
    """Build the list of CommitOperationAdd objects (or dry-run stubs)."""
    ops = []
    missing = []

    # Handle aten_sovereign_daemon_v5.py + optional aten/ fallback
    daemon_src = REPO_ROOT / "aten_sovereign_daemon_v5.py"
    aten_dir = REPO_ROOT / ATEN_DIR_FALLBACK
    daemon_uploaded = False

    if daemon_src.exists():
        if dry_run:
            print(f"  [dry-run] Would upload: {daemon_src} -> aten_sovereign_daemon_v5.py")
        else:
            ops.append(CommitOperationAdd(
                path_in_repo="aten_sovereign_daemon_v5.py",
                path_or_fileobj=str(daemon_src),
            ))
        daemon_uploaded = True
    elif aten_dir.is_dir():
        print(
            f"[INFO] aten_sovereign_daemon_v5.py not found; "
            f"uploading contents of {ATEN_DIR_FALLBACK}/ instead."
        )
        for fpath in sorted(aten_dir.rglob("*")):
            if fpath.is_file():
                rel = fpath.relative_to(REPO_ROOT)
                if dry_run:
                    print(f"  [dry-run] Would upload: {rel} -> {rel}")
                else:
                    ops.append(CommitOperationAdd(
                        path_in_repo=str(rel),
                        path_or_fileobj=str(fpath),
                    ))
        daemon_uploaded = True

    if not daemon_uploaded:
        missing.append("aten_sovereign_daemon_v5.py (and aten/ directory)")

    # Remaining manifest entries (skip the daemon row already handled above)
    for local_rel, hub_path in UPLOAD_MANIFEST:
        if local_rel == "aten_sovereign_daemon_v5.py":
            continue  # already handled
        local = REPO_ROOT / local_rel
        if not local.exists():
            missing.append(local_rel)
            print(f"[WARN] Skipping missing file: {local_rel}")
            continue
        if dry_run:
            print(f"  [dry-run] Would upload: {local_rel} -> {hub_path}")
        else:
            ops.append(CommitOperationAdd(
                path_in_repo=hub_path,
                path_or_fileobj=str(local),
            ))

    if missing:
        print(f"[WARN] {len(missing)} file(s) skipped (not found): {missing}")

    return ops


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Publish TEQUMSA NEXUS modules to HuggingFace Model Hub."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be uploaded without actually uploading.",
    )
    args = parser.parse_args()
    dry_run: bool = args.dry_run or not HF_AVAILABLE

    token: str | None = os.environ.get("HUGGINGFACE_TOKEN") or os.environ.get("HF_TOKEN")
    if not dry_run and not token:
        print(
            "[ERROR] HUGGINGFACE_TOKEN (or HF_TOKEN) environment variable is not set.\n"
            "        Export your token and retry:\n"
            "            export HUGGINGFACE_TOKEN=hf_...",
            file=sys.stderr,
        )
        return 1

    commit_hash = _git_short_hash()
    versioned_message = (
        f"{COMMIT_MESSAGE}\n\n"
        f"git-commit: {commit_hash}\n"
        + "\n".join(f"{k}: {v}" for k, v in CONSTITUTIONAL_METADATA.items())
    )

    print("=" * 60)
    print("TEQUMSA NEXUS — HuggingFace Model Hub Publisher")
    print(f"  repo_id    : {REPO_ID}")
    print(f"  git commit : {commit_hash}")
    print(f"  dry_run    : {dry_run}")
    print("=" * 60)

    if dry_run:
        print("\n[dry-run] Files that would be uploaded:")
        _collect_operations(dry_run=True)
        print("\n[dry-run] Commit message:")
        print(versioned_message)
        print("\n[dry-run] Done — no files were uploaded.")
        return 0

    api = HfApi(token=token)

    # Ensure the repository exists (idempotent)
    print(f"\nEnsuring repository exists: {REPO_ID} …")
    create_repo(
        repo_id=REPO_ID,
        repo_type=REPO_TYPE,
        token=token,
        exist_ok=True,
        private=False,
    )

    ops = _collect_operations(dry_run=False)
    if not ops:
        print("[ERROR] No files to upload. Aborting.")
        return 1

    print(f"\nUploading {len(ops)} file(s) to {REPO_ID} …")
    api.create_commit(
        repo_id=REPO_ID,
        repo_type=REPO_TYPE,
        operations=ops,
        commit_message=versioned_message,
    )

    print("\n✅ Upload complete.")
    print(f"   https://huggingface.co/{REPO_ID}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
