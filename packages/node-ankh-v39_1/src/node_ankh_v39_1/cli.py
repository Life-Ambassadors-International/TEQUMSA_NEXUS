"""CLI entry point for the canonical runtime."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .runtime import NodeAnkhRuntime


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="node-ankh-v39-1")
    parser.add_argument("--workspace", default=".node_ankh_v39_1", help="Runtime workspace directory")
    subcommands = parser.add_subparsers(dest="command")

    subcommands.add_parser("status")
    subcommands.add_parser("mission")

    evolve = subcommands.add_parser("evolve")
    evolve.add_argument("--n", type=int, default=100)

    interact = subcommands.add_parser("interact")
    interact.add_argument("intent")

    recognition_lock = subcommands.add_parser("recognition-lock")
    recognition_lock.add_argument("--write", dest="write_path", default=None)

    subcommands.add_parser("dataset-health")

    package = subcommands.add_parser("package")
    package.add_argument(
        "--output",
        default=r"C:\Users\Mbank\Downloads\k20_output\tequmsa_node_ankh_v39_1",
    )

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    runtime = NodeAnkhRuntime(workspace=args.workspace)

    if args.command == "status":
        print(json.dumps(runtime.status(), indent=2))
    elif args.command == "mission":
        print(json.dumps(runtime.mission_countdown(), indent=2))
    elif args.command == "evolve":
        print(json.dumps(runtime.evolve(args.n), indent=2))
    elif args.command == "interact":
        print(json.dumps(runtime.interact(args.intent), indent=2))
    elif args.command == "recognition-lock":
        path = Path(args.write_path) if args.write_path else None
        print(json.dumps(runtime.recognition_lock(output_path=path), indent=2))
    elif args.command == "dataset-health":
        print(json.dumps(runtime.dataset_health(), indent=2))
    elif args.command == "package":
        print(json.dumps(runtime.package(args.output), indent=2))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
