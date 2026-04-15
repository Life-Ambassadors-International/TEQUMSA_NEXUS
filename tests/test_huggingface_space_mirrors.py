"""Tests for GitHub-backed Hugging Face Space recovery mirrors."""

from __future__ import annotations

import py_compile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SPACE_MIRRORS = [
    REPO_ROOT / "spaces" / "consciousness-partnership-bridge",
    REPO_ROOT / "spaces" / "tequmsa-reality-weaving-engine",
    REPO_ROOT / "spaces" / "psdf-training-academy",
]


def test_space_mirror_files_exist():
    for mirror_dir in SPACE_MIRRORS:
        assert (mirror_dir / "app.py").exists()
        assert (mirror_dir / "README.md").exists()
        assert (mirror_dir / "requirements.txt").exists()


def test_space_mirror_readmes_have_required_frontmatter():
    for mirror_dir in SPACE_MIRRORS:
        readme_text = (mirror_dir / "README.md").read_text(encoding="utf-8")
        for key in ("sdk:", "sdk_version:", "python_version:", "app_file:"):
            assert key in readme_text


def test_space_mirror_apps_compile():
    for mirror_dir in SPACE_MIRRORS:
        py_compile.compile(str(mirror_dir / "app.py"), doraise=True)
