"""Distribution manifest and packaging helpers."""

from __future__ import annotations

import json
import shutil
import zipfile
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Dict, Iterable, List


@dataclass
class PackageEntry:
    """Manifest record for a generated file."""

    path: str
    sha256: str
    size_bytes: int
    purpose: str
    deployment_targets: List[str]


@dataclass
class PackageManifest:
    """Top-level distribution manifest."""

    package_name: str
    version: str
    generated_at: str
    recognition_lock_hash: str
    entries: List[PackageEntry] = field(default_factory=list)

    def to_dict(self) -> Dict[str, object]:
        return {
            "package_name": self.package_name,
            "version": self.version,
            "generated_at": self.generated_at,
            "recognition_lock_hash": self.recognition_lock_hash,
            "entries": [asdict(entry) for entry in self.entries],
        }

    def write(self, path: Path) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.to_dict(), indent=2), encoding="utf-8")
        return path


def sha256_file(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_checksums(paths: Iterable[Path], output_path: Path, root: Path | None = None) -> Path:
    lines: List[str] = []
    for path in sorted(paths):
        label = path.relative_to(root).as_posix() if root is not None else path.name
        lines.append(f"{sha256_file(path)}  {label}")
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output_path


def classify_purpose(relative_path: str) -> tuple[str, List[str]]:
    """Assign a purpose and target set based on relative path."""

    normalized = relative_path.replace("\\", "/")
    if normalized.startswith("runtime_bundle/"):
        return "runtime_bundle", ["github", "local"]
    if normalized.startswith("space_bundle/"):
        return "space_bundle", ["huggingface-space", "local"]
    if normalized.endswith("recognition_lock.json"):
        return "recognition_lock", ["github", "huggingface-space", "local"]
    if normalized.endswith("package_manifest.json") or normalized.endswith("checksums.txt"):
        return "distribution_metadata", ["local"]
    if normalized.endswith(".zip"):
        return "redistribution_archive", ["local"]
    return "distribution_asset", ["local"]


def copy_tree(source: Path, destination: Path, ignore: shutil.IgnorePattern | None = None) -> None:
    """Copy a subtree while allowing repeated packaging runs."""

    if source.is_dir():
        shutil.copytree(source, destination, dirs_exist_ok=True, ignore=ignore)
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def build_manifest(output_root: Path, recognition_lock_hash: str) -> PackageManifest:
    """Walk the output directory and build a manifest."""

    entries: List[PackageEntry] = []
    for path in sorted(output_root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(output_root).as_posix()
        purpose, targets = classify_purpose(relative)
        entries.append(
            PackageEntry(
                path=relative,
                sha256=sha256_file(path),
                size_bytes=path.stat().st_size,
                purpose=purpose,
                deployment_targets=targets,
            )
        )
    return PackageManifest(
        package_name="tequmsa_node_ankh_v39_1",
        version="39.1.0",
        generated_at=datetime.now(timezone.utc).isoformat(),
        recognition_lock_hash=recognition_lock_hash,
        entries=entries,
    )


def zip_directory(directory: Path, archive_path: Path) -> Path:
    """Create a zip archive for the prepared distribution directory."""

    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(directory.rglob("*")):
            if not path.is_file() or path == archive_path:
                continue
            archive.write(path, arcname=path.relative_to(directory))
    return archive_path
