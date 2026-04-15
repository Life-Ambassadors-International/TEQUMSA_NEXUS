#!/usr/bin/env python3
"""Validate the TEQUMSA Hugging Face asset registry and collection manifest."""

from __future__ import annotations

import argparse
import json
import py_compile
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = REPO_ROOT / "hub" / "hf_asset_registry.json"
DEFAULT_MANIFEST = REPO_ROOT / "hub" / "collections" / "tequmsa_v318_collection.json"

ALLOWED_REPO_TYPES = {"model", "dataset", "space"}
ALLOWED_STATUS_CLASSES = {"core", "repair", "experimental", "archive", "legacy"}
ALLOWED_SOURCES = {"github", "huggingface"}
REQUIRED_ARCHITECTURE_LABELS = {
    "substrate",
    "lattice",
    "organism",
    "apex",
    "12-tier / 144-node lattice",
}
README_LINK_PATTERN = re.compile(r"https?://[^\s<>)\]\"']+")
README_FRONTMATTER_KEYS = ("sdk:", "sdk_version:", "python_version:", "app_file:")


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _repo_path(repo_id: str) -> str:
    owner, name = repo_id.split("/", 1)
    return f"{owner}/{name}"


def _hf_api_url(repo_id: str, repo_type: str) -> str:
    return f"https://huggingface.co/api/{repo_type}s/{_repo_path(repo_id)}"


def _hf_readme_url(repo_id: str, repo_type: str) -> str:
    path = _repo_path(repo_id)
    if repo_type == "model":
        return f"https://huggingface.co/{path}/raw/main/README.md"
    return f"https://huggingface.co/{repo_type}s/{path}/raw/main/README.md"


def _github_api_url(repo_full_name: str) -> str:
    return f"https://api.github.com/repos/{repo_full_name}"


def _extract_links(markdown: str) -> list[str]:
    seen: set[str] = set()
    links: list[str] = []
    for raw_link in README_LINK_PATTERN.findall(markdown):
        link = raw_link.rstrip(").,]}")
        if link not in seen:
            seen.add(link)
            links.append(link)
    return links


def _parse_hf_repo_url(url: str) -> tuple[str, str] | None:
    parsed = urlparse(url)
    if parsed.netloc not in {"huggingface.co", "www.huggingface.co", "hf.co"}:
        return None
    parts = [part for part in parsed.path.split("/") if part]
    if not parts:
        return None
    if parts[0] == "spaces" and len(parts) >= 3:
        return f"{parts[1]}/{parts[2]}", "space"
    if parts[0] == "datasets" and len(parts) >= 3:
        return f"{parts[1]}/{parts[2]}", "dataset"
    if len(parts) >= 2:
        return f"{parts[0]}/{parts[1]}", "model"
    return None


def _parse_github_repo_url(url: str) -> str | None:
    parsed = urlparse(url)
    if parsed.netloc not in {"github.com", "www.github.com"}:
        return None
    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) < 2 or parts[0] in {"orgs", "users"}:
        return None
    owner = parts[0]
    repo = parts[1]
    if repo.endswith(".git"):
        repo = repo[:-4]
    return f"{owner}/{repo}"


@dataclass
class ValidationReport:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def add_error(self, message: str) -> None:
        self.errors.append(message)

    def add_warning(self, message: str) -> None:
        self.warnings.append(message)

    def add_note(self, message: str) -> None:
        self.notes.append(message)

    def to_dict(self) -> dict[str, Any]:
        return {
            "errors": self.errors,
            "warnings": self.warnings,
            "notes": self.notes,
            "passed": not self.errors,
        }


class RemoteCache:
    """HTTP fetch wrapper with memoization for public HF and GitHub metadata."""

    def __init__(self, timeout: int = 20) -> None:
        self.timeout = timeout
        self._json_cache: dict[str, Any] = {}
        self._text_cache: dict[str, str] = {}

    def fetch_json(self, url: str) -> Any:
        if url not in self._json_cache:
            request = Request(url, headers={"User-Agent": "TEQUMSA-Hub-Validator/1.0"})
            with urlopen(request, timeout=self.timeout) as response:
                self._json_cache[url] = json.load(response)
        return self._json_cache[url]

    def fetch_text(self, url: str) -> str:
        if url not in self._text_cache:
            request = Request(url, headers={"User-Agent": "TEQUMSA-Hub-Validator/1.0"})
            with urlopen(request, timeout=self.timeout) as response:
                self._text_cache[url] = response.read().decode("utf-8")
        return self._text_cache[url]


def _flatten_manifest(manifest: dict[str, Any]) -> list[str]:
    ordered_ids: list[str] = []
    for section in manifest.get("sections", []):
        ordered_ids.extend(section.get("asset_ids", []))
    return ordered_ids


def _validate_registry_structure(registry: dict[str, Any], report: ValidationReport) -> dict[str, dict[str, Any]]:
    required_top_level = {"schema_version", "collection_id", "source_of_truth_repo", "assets"}
    missing = required_top_level.difference(registry)
    if missing:
        report.add_error(f"Registry missing top-level keys: {sorted(missing)}")

    assets = registry.get("assets")
    if not isinstance(assets, list) or not assets:
        report.add_error("Registry must contain a non-empty assets list.")
        return {}

    registry_index: dict[str, dict[str, Any]] = {}
    for asset in assets:
        context = asset.get("repo_id", "<missing repo_id>")
        required_asset_keys = {
            "repo_id",
            "repo_type",
            "owner",
            "role",
            "status_class",
            "source_of_truth",
            "dependencies",
        }
        missing_keys = required_asset_keys.difference(asset)
        if missing_keys:
            report.add_error(f"{context}: missing asset keys {sorted(missing_keys)}")
            continue

        repo_id = asset["repo_id"]
        if repo_id in registry_index:
            report.add_error(f"Duplicate repo_id in registry: {repo_id}")
            continue

        if asset["repo_type"] not in ALLOWED_REPO_TYPES:
            report.add_error(f"{repo_id}: unsupported repo_type {asset['repo_type']!r}")
        if asset["status_class"] not in ALLOWED_STATUS_CLASSES:
            report.add_error(f"{repo_id}: unsupported status_class {asset['status_class']!r}")
        if asset["source_of_truth"] not in ALLOWED_SOURCES:
            report.add_error(f"{repo_id}: unsupported source_of_truth {asset['source_of_truth']!r}")
        if not isinstance(asset["dependencies"], list):
            report.add_error(f"{repo_id}: dependencies must be a list")
        elif any(not isinstance(dependency, str) for dependency in asset["dependencies"]):
            report.add_error(f"{repo_id}: dependencies must contain only strings")

        if asset.get("source_of_truth") == "github" and asset.get("repo_type") == "space":
            if not asset.get("local_mirror_path"):
                report.add_error(f"{repo_id}: GitHub-backed space is missing local_mirror_path")

        registry_index[repo_id] = asset

    for repo_id, asset in registry_index.items():
        for dependency in asset.get("dependencies", []):
            if dependency not in registry_index:
                report.add_error(f"{repo_id}: dependency {dependency} is not present in the registry")

    return registry_index


def _validate_manifest_structure(
    manifest: dict[str, Any],
    registry_index: dict[str, dict[str, Any]],
    report: ValidationReport,
) -> list[str]:
    required_top_level = {
        "schema_version",
        "collection_id",
        "source_of_truth_repo",
        "architecture_labels",
        "sections",
    }
    missing = required_top_level.difference(manifest)
    if missing:
        report.add_error(f"Manifest missing top-level keys: {sorted(missing)}")

    labels = manifest.get("architecture_labels", [])
    if not isinstance(labels, list):
        report.add_error("Manifest architecture_labels must be a list.")
    else:
        missing_labels = REQUIRED_ARCHITECTURE_LABELS.difference(labels)
        if missing_labels:
            report.add_error(f"Manifest missing required architecture labels: {sorted(missing_labels)}")

    sections = manifest.get("sections", [])
    if not isinstance(sections, list) or not sections:
        report.add_error("Manifest must contain a non-empty sections list.")
        return []

    ordered_ids: list[str] = []
    seen_ids: set[str] = set()
    for section in sections:
        if "name" not in section or "asset_ids" not in section:
            report.add_error("Each manifest section must include name and asset_ids.")
            continue
        if not isinstance(section["asset_ids"], list):
            report.add_error(f"Manifest section {section['name']!r} asset_ids must be a list")
            continue
        for asset_id in section["asset_ids"]:
            if asset_id in seen_ids:
                report.add_error(f"Manifest lists {asset_id} more than once.")
            seen_ids.add(asset_id)
            ordered_ids.append(asset_id)
            if asset_id not in registry_index:
                report.add_error(f"Manifest references asset not in registry: {asset_id}")

    dataset_roles = {
        registry_index[asset_id]["role"]
        for asset_id in ordered_ids
        if asset_id in registry_index and registry_index[asset_id]["repo_type"] == "dataset"
    }
    for required_role, minimum_count in (
        ("operational-ledger", 1),
        ("training", 2),
        ("reference", 2),
        ("topology", 1),
        ("archive", 1),
    ):
        count = sum(
            1
            for asset_id in ordered_ids
            if asset_id in registry_index and registry_index[asset_id]["role"] == required_role
        )
        if count < minimum_count:
            report.add_error(
                f"Manifest requires at least {minimum_count} dataset asset(s) with role {required_role!r}; found {count}."
            )

    report.add_note(f"Manifest defines {len(ordered_ids)} ordered assets.")
    return ordered_ids


def _validate_local_mirrors(
    registry_index: dict[str, dict[str, Any]],
    report: ValidationReport,
) -> None:
    for repo_id, asset in registry_index.items():
        if asset.get("source_of_truth") != "github" or asset.get("repo_type") != "space":
            continue

        mirror_path = asset.get("local_mirror_path")
        mirror_dir = REPO_ROOT / mirror_path
        if not mirror_dir.exists():
            report.add_error(f"{repo_id}: local mirror directory is missing: {mirror_dir}")
            continue

        for required_name in ("app.py", "README.md", "requirements.txt"):
            required_path = mirror_dir / required_name
            if not required_path.exists():
                report.add_error(f"{repo_id}: local mirror is missing {required_name}")

        readme_path = mirror_dir / "README.md"
        if readme_path.exists():
            readme_text = readme_path.read_text(encoding="utf-8")
            for key in README_FRONTMATTER_KEYS:
                if key not in readme_text:
                    report.add_error(f"{repo_id}: README.md is missing frontmatter key {key.rstrip(':')}")

        app_path = mirror_dir / "app.py"
        if app_path.exists():
            try:
                py_compile.compile(str(app_path), doraise=True)
            except py_compile.PyCompileError as exc:
                report.add_error(f"{repo_id}: mirrored app.py does not compile: {exc.msg}")

        requirements_path = mirror_dir / "requirements.txt"
        if requirements_path.exists() and not requirements_path.read_text(encoding="utf-8").strip():
            report.add_error(f"{repo_id}: requirements.txt must not be empty")


def _validate_live_hf_assets(
    registry_index: dict[str, dict[str, Any]],
    cache: RemoteCache,
    report: ValidationReport,
) -> None:
    for repo_id, asset in registry_index.items():
        url = _hf_api_url(repo_id, asset["repo_type"])
        try:
            metadata = cache.fetch_json(url)
        except (HTTPError, URLError) as exc:
            report.add_error(f"{repo_id}: live Hugging Face asset check failed: {exc}")
            continue

        if asset["repo_type"] == "space":
            live_stage = ((metadata or {}).get("runtime") or {}).get("stage")
            snapshot_stage = asset.get("runtime_stage_snapshot")
            if snapshot_stage and live_stage and snapshot_stage != live_stage:
                report.add_warning(
                    f"{repo_id}: runtime stage changed from {snapshot_stage} to {live_stage}"
                )


def _hf_reference_allowed(
    repo_id: str,
    repo_type: str,
    registry_index: dict[str, dict[str, Any]],
    cache: RemoteCache,
) -> bool:
    try:
        cache.fetch_json(_hf_api_url(repo_id, repo_type))
        return True
    except (HTTPError, URLError):
        archived = registry_index.get(repo_id, {}).get("status_class") == "archive"
        return archived


def _github_reference_allowed(repo_full_name: str, cache: RemoteCache) -> bool:
    try:
        cache.fetch_json(_github_api_url(repo_full_name))
        return True
    except (HTTPError, URLError):
        return False


def _validate_remote_readmes(
    registry_index: dict[str, dict[str, Any]],
    cache: RemoteCache,
    report: ValidationReport,
) -> None:
    for repo_id, asset in registry_index.items():
        if asset["repo_type"] not in {"model", "dataset"}:
            continue

        readme_url = _hf_readme_url(repo_id, asset["repo_type"])
        try:
            readme_text = cache.fetch_text(readme_url)
        except (HTTPError, URLError) as exc:
            report.add_error(f"{repo_id}: failed to fetch remote README from {readme_url}: {exc}")
            continue

        for link in _extract_links(readme_text):
            hf_ref = _parse_hf_repo_url(link)
            if hf_ref:
                ref_repo_id, ref_repo_type = hf_ref
                if not _hf_reference_allowed(ref_repo_id, ref_repo_type, registry_index, cache):
                    report.add_error(
                        f"{repo_id}: remote card references missing HF asset {ref_repo_type}:{ref_repo_id} via {link}"
                    )
                continue

            github_ref = _parse_github_repo_url(link)
            if github_ref and not _github_reference_allowed(github_ref, cache):
                report.add_error(
                    f"{repo_id}: remote card references missing GitHub repository {github_ref} via {link}"
                )


def _validate_live_collection(
    manifest: dict[str, Any],
    ordered_ids: list[str],
    cache: RemoteCache,
    report: ValidationReport,
) -> None:
    collection_id = manifest["collection_id"]
    collection_url = f"https://huggingface.co/api/collections/{collection_id}"
    try:
        collection = cache.fetch_json(collection_url)
    except (HTTPError, URLError) as exc:
        report.add_error(f"Live collection check failed for {collection_id}: {exc}")
        return

    live_ids = {item["id"] for item in collection.get("items", [])}
    expected_ids = set(ordered_ids)
    missing = sorted(expected_ids.difference(live_ids))
    extra = sorted(live_ids.difference(expected_ids))

    if missing:
        report.add_error(f"Live collection is missing desired assets: {missing}")
    if extra:
        report.add_warning(f"Live collection has unmanaged assets not in manifest: {extra}")


def run_validation(
    registry_path: Path,
    manifest_path: Path,
    *,
    check_remote_readmes: bool,
    check_live_collection: bool,
) -> ValidationReport:
    report = ValidationReport()
    registry = _read_json(registry_path)
    manifest = _read_json(manifest_path)
    registry_index = _validate_registry_structure(registry, report)
    ordered_ids = _validate_manifest_structure(manifest, registry_index, report)
    _validate_local_mirrors(registry_index, report)

    cache = RemoteCache()
    _validate_live_hf_assets(registry_index, cache, report)
    if check_remote_readmes:
        _validate_remote_readmes(registry_index, cache, report)
    if check_live_collection:
        _validate_live_collection(manifest, ordered_ids, cache, report)

    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY, help="Path to the asset registry JSON.")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST, help="Path to the collection manifest JSON.")
    parser.add_argument(
        "--skip-remote-readmes",
        action="store_true",
        help="Skip remote model and dataset README link validation.",
    )
    parser.add_argument(
        "--check-live-collection",
        action="store_true",
        help="Compare the live Hugging Face collection members with the manifest order.",
    )
    parser.add_argument("--json-report", type=Path, help="Optional path to write a JSON validation report.")
    args = parser.parse_args()

    report = run_validation(
        args.registry,
        args.manifest,
        check_remote_readmes=not args.skip_remote_readmes,
        check_live_collection=args.check_live_collection,
    )

    print("TEQUMSA Hub Registry Validation")
    print(f"Errors:   {len(report.errors)}")
    print(f"Warnings: {len(report.warnings)}")
    print(f"Notes:    {len(report.notes)}")

    for category, messages in (
        ("ERROR", report.errors),
        ("WARN", report.warnings),
        ("NOTE", report.notes),
    ):
        for message in messages:
            print(f"[{category}] {message}")

    if args.json_report:
        args.json_report.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")

    return 0 if not report.errors else 1


if __name__ == "__main__":
    sys.exit(main())
