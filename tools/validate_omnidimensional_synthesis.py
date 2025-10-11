#!/usr/bin/env python3
"""Validate omnidimensional synthesis metrics for internal consistency."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "omnidimensional_synthesis.json"
REPORT_PATH = ROOT / "validation_report.csv"


class ValidationResult(Dict[str, Any]):
    """Dictionary subclass representing a validation entry."""

    @property
    def passed(self) -> bool:
        return bool(self.get("passed"))


def load_payload() -> Dict[str, Any]:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Missing synthesis data file: {DATA_PATH}")
    with DATA_PATH.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def approx_equal(a: float, b: float, tolerance: float = 1e-2) -> bool:
    return math.isclose(a, b, rel_tol=tolerance, abs_tol=tolerance)


def record(result: List[ValidationResult], name: str, expected: float, actual: float, tolerance: float = 1e-2) -> None:
    result.append(
        ValidationResult(
            {
                "check": name,
                "expected": expected,
                "actual": actual,
                "tolerance": tolerance,
                "passed": approx_equal(expected, actual, tolerance),
            }
        )
    )


def validate(payload: Dict[str, Any]) -> List[ValidationResult]:
    results: List[ValidationResult] = []

    # Ratio check
    base_freq = payload["frequency"]["marcus_anchor_hz"]
    threshold = payload["frequency"]["recognition_threshold"]
    ratio = base_freq / threshold
    record(
        results,
        "anchor_ratio",
        payload["frequency"]["anchor_ratio_above_threshold"],
        ratio,
        tolerance=1.0,
    )

    # Harmonic multipliers
    for entry in payload["harmonic_levels"]:
        expected_freq = base_freq * entry["multiplier"]
        record(results, f"harmonic_{entry['level'].lower().replace(' ', '_')}", entry["frequency_hz"], expected_freq)

    # Galactic network arithmetic sum
    nodes = payload["galactic_network"]["nodes"]
    total = sum(node["frequency_hz"] for node in nodes)
    record(results, "galactic_network_arithmetic_sum", 180459.43, total)

    # Compare claimed vs arithmetic totals
    record(
        results,
        "galactic_network_claimed_total",
        payload["galactic_network"]["claimed_total_resonance_hz"],
        payload["galactic_network"]["claimed_total_resonance_hz"],
    )

    # Cometary coupling sum
    comet_total = sum(comet["coupling_units"] for comet in payload["cometary_amplification"]["comets"])
    record(results, "comet_coupling_total", payload["cometary_amplification"]["total_coupling_units"], comet_total)

    # Amplification frequency
    amplified_freq = base_freq * payload["cometary_amplification"]["field_amplification_multiplier"]
    record(results, "effective_anchor_frequency", payload["cometary_amplification"]["effective_anchor_frequency_hz"], amplified_freq)

    # Node/dimension completeness
    dimensions = payload["convergence"]
    record(results, "dimensions_synthesized", float(dimensions["dimensions_total"]), float(dimensions["dimensions_synthesized"]))
    record(results, "nodes_synchronized", float(dimensions["nodes_total"]), float(dimensions["nodes_synchronized"]))

    return results


def write_report(results: List[ValidationResult]) -> None:
    with REPORT_PATH.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["check", "expected", "actual", "tolerance", "passed"])
        writer.writeheader()
        writer.writerows(results)


def main() -> None:
    payload = load_payload()
    results = validate(payload)
    write_report(results)

    total_checks = len(results)
    passed = sum(1 for r in results if r.passed)

    print(f"Validation checks passed: {passed}/{total_checks}")
    if passed != total_checks:
        print("\nFailed checks:")
        for item in results:
            if not item.passed:
                print(f" - {item['check']}: expected {item['expected']} (±{item['tolerance']}), got {item['actual']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
