#!/usr/bin/env python3
"""Workflow wrapper for TEQUMSA lattice synthesis."""

from __future__ import annotations

import json
import sys

from core.swarm_omnisynthesis import swarm_synthesis


def main() -> int:
    node_name = sys.argv[1] if len(sys.argv) > 1 else "TEQUMSA_NEXUS"
    result = swarm_synthesis(node=node_name)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
