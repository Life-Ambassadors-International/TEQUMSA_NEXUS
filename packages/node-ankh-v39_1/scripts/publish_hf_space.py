"""Explicit Hugging Face Space publish helper."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-id", default="Mbanksbey/TEQUMSA-Constitutional-Validator")
    parser.add_argument("--space-root", default=str(Path(__file__).resolve().parents[1] / "space"))
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()

    print(f"repo_id={args.repo_id}")
    print(f"space_root={Path(args.space_root).resolve()}")
    if not args.execute:
        print("Dry run only. Re-run with --execute after installing huggingface_hub and setting HF_TOKEN.")
        return

    from huggingface_hub import HfApi

    api = HfApi(token=None)
    api.upload_folder(
        repo_id=args.repo_id,
        repo_type="space",
        folder_path=str(Path(args.space_root).resolve()),
        commit_message="Update TEQUMSA Constitutional Validator from canonical v39.1 package",
    )


if __name__ == "__main__":
    main()
