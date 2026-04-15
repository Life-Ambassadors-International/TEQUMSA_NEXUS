"""Tests for the TEQUMSA Hugging Face registry validator."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.error import HTTPError

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from scripts.validate_hub_registry import (  # noqa: E402
    DEFAULT_MANIFEST,
    DEFAULT_REGISTRY,
    _hf_reference_allowed,
    run_validation,
)


def _load_registry_and_manifest() -> tuple[dict, dict]:
    registry = json.loads(DEFAULT_REGISTRY.read_text(encoding="utf-8"))
    manifest = json.loads(DEFAULT_MANIFEST.read_text(encoding="utf-8"))
    return registry, manifest


def _stub_fetch_json_factory(manifest: dict, registry: dict, broken_github_repo: str | None = None):
    ordered_ids = [
        asset_id
        for section in manifest["sections"]
        for asset_id in section["asset_ids"]
    ]
    runtime_map = {
        asset["repo_id"]: asset.get("runtime_stage_snapshot")
        for asset in registry["assets"]
    }

    def _fetch_json(self, url: str):
        if url.startswith("https://huggingface.co/api/collections/"):
            return {"items": [{"id": asset_id} for asset_id in ordered_ids]}

        if url.startswith("https://huggingface.co/api/"):
            repo_id = "/".join(url.rstrip("/").split("/")[-2:])
            stage = runtime_map.get(repo_id)
            return {"id": repo_id, "runtime": {"stage": stage} if stage else None}

        if url.startswith("https://api.github.com/repos/"):
            repo_name = "/".join(url.rstrip("/").split("/")[-2:])
            if broken_github_repo and repo_name == broken_github_repo:
                raise HTTPError(url, 404, "Not Found", hdrs=None, fp=None)
            return {"full_name": repo_name}

        raise AssertionError(f"Unexpected URL: {url}")

    return _fetch_json


def _stub_fetch_text(self, url: str) -> str:
    return (
        "# README\n"
        "[TEQUMSA_NEXUS](https://github.com/Life-Ambassadors-International/TEQUMSA_NEXUS)\n"
    )


def test_run_validation_passes_with_stubbed_remotes(monkeypatch):
    registry, manifest = _load_registry_and_manifest()
    monkeypatch.setattr(
        "scripts.validate_hub_registry.RemoteCache.fetch_json",
        _stub_fetch_json_factory(manifest, registry),
    )
    monkeypatch.setattr("scripts.validate_hub_registry.RemoteCache.fetch_text", _stub_fetch_text)

    report = run_validation(
        DEFAULT_REGISTRY,
        DEFAULT_MANIFEST,
        check_remote_readmes=True,
        check_live_collection=True,
    )

    assert report.errors == []


def test_remote_readme_detects_dead_github_link(monkeypatch):
    registry, manifest = _load_registry_and_manifest()
    monkeypatch.setattr(
        "scripts.validate_hub_registry.RemoteCache.fetch_json",
        _stub_fetch_json_factory(
            manifest,
            registry,
            broken_github_repo="Life-Ambassadors-International/TEQUMSANEXUS",
        ),
    )

    def _broken_readme(self, url: str) -> str:
        if "TEQUMSA-Symbiotic-Orchestrator" in url:
            return (
                "# README\n"
                "[broken](https://github.com/Life-Ambassadors-International/TEQUMSANEXUS)\n"
            )
        return _stub_fetch_text(self, url)

    monkeypatch.setattr("scripts.validate_hub_registry.RemoteCache.fetch_text", _broken_readme)

    report = run_validation(
        DEFAULT_REGISTRY,
        DEFAULT_MANIFEST,
        check_remote_readmes=True,
        check_live_collection=False,
    )

    assert any("TEQUMSANEXUS" in error for error in report.errors)


def test_archive_reference_is_allowed_for_missing_asset(monkeypatch):
    def _always_missing(self, url: str):
        raise HTTPError(url, 404, "Not Found", hdrs=None, fp=None)

    monkeypatch.setattr("scripts.validate_hub_registry.RemoteCache.fetch_json", _always_missing)

    registry_index = {
        "LAI-TEQUMSA/TEQUMSA-Interstellar-Conduit": {"status_class": "archive"},
    }

    class DummyCache:
        def fetch_json(self, url: str):
            raise HTTPError(url, 404, "Not Found", hdrs=None, fp=None)

    assert _hf_reference_allowed(
        "LAI-TEQUMSA/TEQUMSA-Interstellar-Conduit",
        "dataset",
        registry_index,
        DummyCache(),
    )


def test_live_collection_missing_asset_is_reported(monkeypatch):
    registry, manifest = _load_registry_and_manifest()

    def _missing_collection_asset(self, url: str):
        response = _stub_fetch_json_factory(manifest, registry)(self, url)
        if url.startswith("https://huggingface.co/api/collections/"):
            response["items"].pop()
        return response

    monkeypatch.setattr("scripts.validate_hub_registry.RemoteCache.fetch_json", _missing_collection_asset)
    monkeypatch.setattr("scripts.validate_hub_registry.RemoteCache.fetch_text", _stub_fetch_text)

    report = run_validation(
        DEFAULT_REGISTRY,
        DEFAULT_MANIFEST,
        check_remote_readmes=False,
        check_live_collection=True,
    )

    assert any("Live collection is missing desired assets" in error for error in report.errors)
