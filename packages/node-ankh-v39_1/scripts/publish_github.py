"""Explicit GitHub publish helper for the checked-out repository."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

PACKAGE_PATH = Path("packages/node-ankh-v39_1")


def run(command: list[str], cwd: Path) -> None:
    subprocess.run(command, cwd=cwd, check=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=str(Path(__file__).resolve().parents[3]))
    parser.add_argument("--branch", default="node-ankh-v39_1-consolidation")
    parser.add_argument("--message", default="Add canonical NODE-ANKH-AN-ATEN v39.1 package")
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    print(f"repo_root={repo_root}")
    print(f"branch={args.branch}")
    print(f"message={args.message}")
    print(f"staged_path={PACKAGE_PATH}")
    if not args.execute:
        print("Dry run only. Re-run with --execute to create a branch, commit, and push.")
        return

    run(["git", "checkout", "-b", args.branch], cwd=repo_root)
    run(["git", "add", str(PACKAGE_PATH), "tests/test_node_ankh_v39_1.py"], cwd=repo_root)
    run(["git", "commit", "-m", args.message], cwd=repo_root)
    run(["git", "push", "-u", "origin", args.branch], cwd=repo_root)


if __name__ == "__main__":
    main()
