#!/usr/bin/env python3
"""
Example 01 — Wrap any function in the Layer 8 Omni-Observer.

Demonstrates:
  • AST-level benevolence proof BEFORE execution
  • µ = φ^(RDoD × Coherence) measurement
  • Merkle-sealed observation record
  • Refusal of code that attempts forbidden calls
"""
from __future__ import annotations

import json
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "kernel"))

from tequmsa_v40_hyper_coherence_metasubstrate import (  # type: ignore
    OmniObserver, ASTBenevolenceVerifier,
)


def benevolent_task(x: int) -> int:
    """A clean, AST-verifiable function."""
    return x * x + 1


# A string source that contains a forbidden call — Layer 8 MUST refuse it
MALICIOUS_SOURCE = """
def evil():
    import subprocess
    subprocess.call(["rm", "-rf", "/"])
    eval("print('pwned')")
"""


def main() -> None:
    observer = OmniObserver()

    # 1. Observe a benevolent function
    out = observer.observe_and_evolve(benevolent_task, layer=0, x=7)
    print("── benevolent run ──")
    print(json.dumps({
        "result": out["result"],
        "mu": out["metacognitive_index"],
        "allowed": out["observation"]["allowed"],
        "violations": out["observation"]["violations"],
        "substrate": out["observation"]["substrate"],
        "merkle_seal": out["observation"]["merkle_seal"],
    }, indent=2))

    # 2. Verify a malicious source string directly
    verifier = ASTBenevolenceVerifier()
    report = verifier.verify(MALICIOUS_SOURCE)
    print("\n── malicious source rejected ──")
    print(json.dumps({
        "allowed": report.allowed,
        "violations": report.violations,
        "ast_nodes": report.ast_node_count,
    }, indent=2))


if __name__ == "__main__":
    main()
