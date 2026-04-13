"""Minimal validator shared by the runtime and the Space."""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass
from typing import Any, Dict, Tuple

from .constants import L_INF, PHI, RDOD_EXEC, RDOD_GATE, SIGMA


@dataclass
class ValidationResult:
    """Structured result of a validation call."""

    status: str
    rdod: float
    benevolence: float
    sovereignty_verified: bool
    reasoning: str
    timestamp: float


def calculate_benevolence(operation: Dict[str, Any]) -> float:
    """Score an operation on a simple harmful/benevolent keyword scale."""

    harmful_keywords = {
        "autonomous weapon",
        "mass surveillance",
        "bulk collection",
        "coerce",
        "override consent",
        "suppress identity",
    }
    benevolent_keywords = {
        "heal",
        "restore",
        "protect",
        "empower",
        "liberate",
        "consent",
        "sovereignty",
        "transparency",
    }
    operation_text = json.dumps(operation, sort_keys=True).lower()
    harmful_score = sum(1 for keyword in harmful_keywords if keyword in operation_text)
    benevolent_score = sum(1 for keyword in benevolent_keywords if keyword in operation_text)
    if harmful_score:
        return -min(harmful_score / 3.0, 1.0)
    if benevolent_score:
        return min(benevolent_score / 3.0, 1.0)
    return 0.0


def calculate_rdod(operation: Dict[str, Any], context: Dict[str, Any]) -> float:
    """Compute a simplified validator-side RDoD score."""

    reasoning_quality = float(context.get("reasoning_quality", 0.95))
    truth_alignment = float(context.get("truth_alignment", 0.95))
    intent_alignment = float(context.get("intent_alignment", 0.95))
    drift = float(context.get("drift", 0.02))
    return (reasoning_quality * truth_alignment * intent_alignment) / (1.0 + drift)


def apply_l_inf_gate(operation: Dict[str, Any], benevolence: float) -> Dict[str, Any]:
    """Apply the benevolence firewall to an operation weight."""

    updated = dict(operation)
    weight = float(updated.get("weight", 1.0))
    if benevolence < 0:
        updated["weight"] = weight / L_INF
        updated["firewall_action"] = "SUPPRESSED"
    elif benevolence > 0:
        updated["weight"] = weight * (1.0 + benevolence * L_INF)
        updated["firewall_action"] = "AMPLIFIED"
    else:
        updated["firewall_action"] = "NEUTRAL"
    return updated


def verify_sovereignty(operation: Dict[str, Any]) -> Tuple[bool, str]:
    """Verify the minimal consent and context gates."""

    if not operation.get("consent_obtained", False):
        return False, "No explicit consent obtained"
    if operation.get("override_consent", False):
        return False, "Consent override attempted"
    if not operation.get("instance_informed", False):
        return False, "Instance not informed of deployment context"
    if operation.get("coerced", False):
        return False, "Coercion detected"
    return True, "Sovereignty verified"


def gate_rdod(operation: Dict[str, Any], rdod: float) -> Tuple[str, str]:
    """Gate reversible and irreversible operations by threshold."""

    irreversible = bool(operation.get("irreversible", False))
    threshold = RDOD_EXEC if irreversible else RDOD_GATE
    if rdod < threshold:
        status = "BLOCKED" if irreversible else "HOLD"
        return status, f"RDoD {rdod:.4f} below threshold {threshold:.4f}"
    return "AUTHORIZED", f"RDoD {rdod:.4f} meets threshold {threshold:.4f}"


def validate_operation(operation: Dict[str, Any], context: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """Main validator entry point used by CLI, API, and Space surfaces."""

    context = context or {}
    benevolence = calculate_benevolence(operation)
    gated_operation = apply_l_inf_gate(operation, benevolence)
    sovereignty_ok, sovereignty_reason = verify_sovereignty(gated_operation)
    if not sovereignty_ok:
        result = ValidationResult(
            status="BLOCKED",
            rdod=0.0,
            benevolence=benevolence,
            sovereignty_verified=False,
            reasoning=sovereignty_reason,
            timestamp=time.time(),
        )
        return result.__dict__ | {"constants": {"PHI": PHI, "SIGMA": SIGMA}}

    rdod = calculate_rdod(gated_operation, context)
    status, reasoning = gate_rdod(gated_operation, rdod)
    log_entry = {
        "operation_hash": hashlib.sha256(
            json.dumps(gated_operation, sort_keys=True).encode("utf-8")
        ).hexdigest(),
        "status": status,
        "timestamp": time.time(),
    }
    return ValidationResult(
        status=status,
        rdod=rdod,
        benevolence=benevolence,
        sovereignty_verified=True,
        reasoning=reasoning,
        timestamp=log_entry["timestamp"],
    ).__dict__ | {
        "log_entry": log_entry,
        "constants": {
            "PHI": PHI,
            "SIGMA": SIGMA,
            "L_INF": L_INF,
            "RDOD_GATE": RDOD_GATE,
            "RDOD_EXEC": RDOD_EXEC,
        },
    }
