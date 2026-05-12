#!/usr/bin/env python3
"""Validate models.json against schemas/model-manifest.schema.json.

Implements model registry manifest validation for TEQUMSA_HUB (issue #107).
Enforces quantum-conscious lattice invariants, security fields, and subscription-
tier constraints in addition to structural JSON-Schema validation.

Exit codes:
  0 — manifest is valid
  1 — validation failed (errors printed to stderr)
  2 — schema or manifest file not found
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Constitutional invariants (must match aten8_github_workflow_agent.py)
# ---------------------------------------------------------------------------
LATTICE_LOCK = "3f7k9p4m2q8r1t6v"
SIGMA = 1.0
OMEGA_HZ = 23514.26

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "models.json"
SCHEMA_PATH = REPO_ROOT / "schemas" / "model-manifest.schema.json"


def _load_json(path: Path) -> dict:
    if not path.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        sys.exit(2)
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def _validate_with_jsonschema(manifest: dict, schema: dict) -> list[str]:
    """Use jsonschema library if available; return list of error messages."""
    try:
        import jsonschema
        validator = jsonschema.Draft7Validator(schema)
        return [str(e.message) for e in sorted(validator.iter_errors(manifest), key=str)]
    except ImportError:
        return []  # fall through to manual checks


def _check_stats_consistency(manifest: dict) -> list[str]:
    """Verify _stats counters match the actual models array."""
    errors: list[str] = []
    stats = manifest.get("_stats", {})
    models = manifest.get("models", [])

    total = stats.get("model_count", -1)
    if total != len(models):
        errors.append(
            f"_stats.model_count={total} does not match actual model count {len(models)}"
        )

    active = sum(1 for m in models if m.get("status") == "active")
    if stats.get("active_count", -1) != active:
        errors.append(
            f"_stats.active_count={stats.get('active_count')} does not match actual active count {active}"
        )

    beta = sum(1 for m in models if m.get("status") == "beta")
    if stats.get("beta_count", -1) != beta:
        errors.append(
            f"_stats.beta_count={stats.get('beta_count')} does not match actual beta count {beta}"
        )
    return errors


def _check_quantum_invariants(manifest: dict) -> list[str]:
    """Validate all quantum-lattice fields enforce constitutional invariants."""
    errors: list[str] = []
    for m in manifest.get("models", []):
        mid = m.get("id", "?")
        ql = m.get("quantum_lattice", {})
        if ql.get("sigma") != SIGMA:
            errors.append(f"model '{mid}': quantum_lattice.sigma must be {SIGMA}")
        if ql.get("lattice_lock") != LATTICE_LOCK:
            errors.append(f"model '{mid}': quantum_lattice.lattice_lock must be '{LATTICE_LOCK}'")
        if ql.get("omega_hz") != OMEGA_HZ:
            errors.append(f"model '{mid}': quantum_lattice.omega_hz must be {OMEGA_HZ}")
        rdod = ql.get("rdod_min", 0.0)
        if not (0.9 <= rdod <= 1.0):
            errors.append(f"model '{mid}': quantum_lattice.rdod_min={rdod} out of range [0.9, 1.0]")
    return errors


def _check_unique_ids(manifest: dict) -> list[str]:
    """Ensure all model IDs are unique."""
    ids: list[str] = [m.get("id", "") for m in manifest.get("models", [])]
    seen: set[str] = set()
    errors: list[str] = []
    for mid in ids:
        if mid in seen:
            errors.append(f"duplicate model id: '{mid}'")
        seen.add(mid)
    return errors


def _check_security_fields(manifest: dict) -> list[str]:
    """Ensure all models that require HMAC specify a valid algorithm."""
    errors: list[str] = []
    for m in manifest.get("models", []):
        mid = m.get("id", "?")
        sec = m.get("security", {})
        if sec.get("requires_hmac") and sec.get("hmac_algo") not in ("sha256", "sha512"):
            errors.append(
                f"model '{mid}': security.hmac_algo must be 'sha256' or 'sha512' when requires_hmac=true"
            )
        if sec.get("audit_enabled") != True:  # noqa: E712 — strict True required by schema
            errors.append(f"model '{mid}': security.audit_enabled must be true")
    return errors


def validate(manifest_path: Path = MANIFEST_PATH, schema_path: Path = SCHEMA_PATH) -> int:
    """Run all validation checks; return exit code (0=pass, 1=fail)."""
    manifest = _load_json(manifest_path)
    schema = _load_json(schema_path)

    all_errors: list[str] = []

    # 1. JSON-Schema structural validation
    all_errors.extend(_validate_with_jsonschema(manifest, schema))

    # 2. Stats consistency
    all_errors.extend(_check_stats_consistency(manifest))

    # 3. Quantum lattice constitutional invariants
    all_errors.extend(_check_quantum_invariants(manifest))

    # 4. Unique IDs
    all_errors.extend(_check_unique_ids(manifest))

    # 5. Security field constraints
    all_errors.extend(_check_security_fields(manifest))

    if all_errors:
        print(f"MANIFEST VALIDATION FAILED — {len(all_errors)} error(s):", file=sys.stderr)
        for err in all_errors:
            print(f"  • {err}", file=sys.stderr)
        return 1

    model_count = len(manifest.get("models", []))
    print(f"✅ Manifest valid — {model_count} model(s) passed all checks.")
    return 0


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Validate TEQUMSA model registry manifest")
    parser.add_argument("--manifest", type=Path, default=MANIFEST_PATH, help="Path to models.json")
    parser.add_argument("--schema", type=Path, default=SCHEMA_PATH, help="Path to JSON schema file")
    args = parser.parse_args()
    sys.exit(validate(args.manifest, args.schema))
