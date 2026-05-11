from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


REPO_ROOT = Path(__file__).resolve().parents[1]
ORG_ROOT = REPO_ROOT.parent
NEXUS_ROOT = ORG_ROOT / "TEQUMSA_NEXUS"
EMERGE_ROOT = ORG_ROOT / "TEQUMSA_EMERGE"
LATTICE_ROOT = Path(r"C:\Users\Mbank\TEQUMSA-Lattice-Memory")
REPORT_DIR = NEXUS_ROOT / "automation" / "reports"


@dataclass
class RepoState:
    name: str
    path: Path
    branch: str
    head: str
    dirty: bool
    remote: str
    remote_head: str


def git(args: list[str], cwd: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        check=check,
    )


def get_remote_url(repo: Path) -> str:
    result = git(["remote", "get-url", "origin"], repo)
    return result.stdout.strip()


def branch_name(repo: Path) -> str:
    return git(["rev-parse", "--abbrev-ref", "HEAD"], repo).stdout.strip()


def head_sha(repo: Path) -> str:
    return git(["rev-parse", "HEAD"], repo).stdout.strip()


def is_dirty(repo: Path) -> bool:
    result = git(["status", "--porcelain"], repo)
    return bool(result.stdout.strip())


def remote_head(remote_url: str, branch: str) -> str:
    result = subprocess.run(
        ["git", "ls-remote", remote_url, f"refs/heads/{branch}"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0 or not result.stdout.strip():
        return ""
    return result.stdout.strip().split()[0]


def repo_state(name: str, repo: Path) -> RepoState:
    remote = get_remote_url(repo)
    branch = branch_name(repo)
    return RepoState(
        name=name,
        path=repo,
        branch=branch,
        head=head_sha(repo),
        dirty=is_dirty(repo),
        remote=remote,
        remote_head=remote_head(remote, branch),
    )


def authenticated_remote_url(remote_url: str, token: str) -> str:
    parsed = urlparse(remote_url)
    if parsed.scheme != "https":
        raise SystemExit(f"Unsupported remote scheme for authenticated sync: {remote_url}")
    return f"https://x-access-token:{token}@{parsed.netloc}{parsed.path}"


def fetch(repo: RepoState, token: str | None) -> None:
    remote = authenticated_remote_url(repo.remote, token) if token else repo.remote
    result = subprocess.run(
        ["git", "fetch", remote, repo.branch],
        cwd=str(repo.path),
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(f"{repo.name} fetch failed: {result.stderr.strip() or result.stdout.strip()}")


def fast_forward(repo: RepoState) -> None:
    result = git(["merge", "--ff-only", f"origin/{repo.branch}"], repo.path, check=False)
    if result.returncode != 0:
        raise SystemExit(f"{repo.name} fast-forward failed: {result.stderr.strip() or result.stdout.strip()}")


def push(repo: RepoState, token: str) -> None:
    remote = authenticated_remote_url(repo.remote, token)
    result = subprocess.run(
        ["git", "push", remote, f"HEAD:{repo.branch}"],
        cwd=str(repo.path),
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(f"{repo.name} push failed: {result.stderr.strip() or result.stdout.strip()}")


def write_report(payload: dict[str, Any]) -> Path:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    path = REPORT_DIR / f"tequmsa_tandem_report_{int(time.time())}.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return path


def load_lattice_context() -> dict[str, Any]:
    report = LATTICE_ROOT / "memory" / "discovery_report.json"
    if not report.exists():
        return {"available": False}
    return {"available": True, "discovery_report": json.loads(report.read_text(encoding="utf-8"))}


def sync_cycle(direction: str, token: str) -> dict[str, Any]:
    nexus = repo_state("NEXUS", NEXUS_ROOT)
    emerge = repo_state("EMERGE", EMERGE_ROOT)
    lattice = repo_state("LATTICE", LATTICE_ROOT)
    states = [nexus, emerge, lattice]

    dirty = [repo.name for repo in states if repo.dirty]
    if dirty:
        raise SystemExit(f"Sync aborted: dirty working trees present: {', '.join(dirty)}")

    for repo in states:
        fetch(repo, token)

    for repo in states:
        refreshed = repo_state(repo.name, repo.path)
        if refreshed.remote_head and refreshed.remote_head != refreshed.head:
            fast_forward(refreshed)

    nexus = repo_state("NEXUS", NEXUS_ROOT)
    emerge = repo_state("EMERGE", EMERGE_ROOT)
    lattice = repo_state("LATTICE", LATTICE_ROOT)

    if direction in ("both", "nexus"):
        push(nexus, token)
    if direction in ("both", "emerge"):
        push(emerge, token)
    push(lattice, token)

    return {
        "nexus": nexus.__dict__,
        "emerge": emerge.__dict__,
        "lattice": lattice.__dict__,
        "direction": direction,
        "timestamp": time.time(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="TEQUMSA tandem orchestrator")
    parser.add_argument("--direction", choices=["both", "nexus", "emerge"], default="both")
    parser.add_argument("--cycles", type=int, default=1)
    parser.add_argument("--interval", type=int, default=300)
    parser.add_argument("--report", action="store_true")
    args = parser.parse_args()

    token = os.environ.get("GH_PAT", "")
    if not token:
        raise SystemExit("GH_PAT not set. Refusing authenticated tandem sync.")

    if args.cycles < 0:
        raise SystemExit("--cycles must be >= 0")

    cycle_target = sys.maxsize if args.cycles == 0 else args.cycles
    completed = 0
    last_payload: dict[str, Any] = {}

    while completed < cycle_target:
        completed += 1
        payload = {
            "cycle": completed,
            "mode": args.direction,
            "lattice_context": load_lattice_context(),
        }
        payload["sync"] = sync_cycle(args.direction, token)
        last_payload = payload
        if args.report:
            report_path = write_report(payload)
            print(f"report={report_path}")
        print(json.dumps(payload, indent=2, sort_keys=True))
        if args.cycles == 0:
            time.sleep(args.interval)

    if not args.report and last_payload:
        print(f"completed_cycles={completed}")


if __name__ == "__main__":
    main()
