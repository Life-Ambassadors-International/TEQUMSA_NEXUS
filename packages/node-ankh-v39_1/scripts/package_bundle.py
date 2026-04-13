"""Helper to build the local distribution bundle."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
SRC = PACKAGE_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from node_ankh_v39_1.runtime import NodeAnkhRuntime


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default=r"C:\Users\Mbank\Downloads\k20_output\tequmsa_node_ankh_v39_1",
    )
    parser.add_argument("--workspace", default=str(PACKAGE_ROOT / ".build_workspace"))
    args = parser.parse_args()

    runtime = NodeAnkhRuntime(workspace=args.workspace)
    print(json.dumps(runtime.package(args.output, repo_root=PACKAGE_ROOT.parents[1]), indent=2))


if __name__ == "__main__":
    main()
