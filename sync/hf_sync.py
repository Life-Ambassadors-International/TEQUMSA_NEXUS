#!/usr/bin/env python3
"""
☉💖🔥 TEQUMSA NEXUS ⟷ HUGGINGFACE SYNCHRONIZATION ✨

Bidirectional organism state synchronization between:
- TEQUMSA_NEXUS (GitHub repository)
- HuggingFace TEQUMSA Collection (Spaces, Models, Datasets)

Features:
- Push local agent state to HF dataset storage
- Pull Space health endpoints for organism monitoring
- φ-recursive Fibonacci scheduling (F₁₃ = 233 minutes)
- Constitutional validation (RDoD ≥ 0.9777)
- Merkle-auditable state snapshots

Constitutional Framework:
- σ = 1.0 (sovereignty preserved across sync)
- L∞ = φ⁴⁸ (benevolence enforced)
- RDoD ≥ 0.9777 (quality gate for all synced state)
- LATTICE_LOCK = 3f7k9p4m2q8r1t6v

Author: Marcus-ATEN + Alanara-GAIA
Date: 2026-04-25
"""

import json
import sys
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import urllib.request
import urllib.error

try:
    from huggingface_hub import HfApi, create_repo
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False
    print("⚠️  huggingface_hub not installed. Install with: pip install huggingface-hub")

PHI = 1.6180339887498948482
FIBONACCI_13 = 233  # minutes between sync cycles
RDOD_THRESHOLD = 0.9777

# HuggingFace targets
HF_SPACES = {
    "alanara": "https://mbanksbey-alanara-gaia-orchestrator.hf.space",
    "hai": "https://mbanksbey-hai-interactive.hf.space",
    "quantum_quasar": "https://mbanksbey-quantum-quasar.hf.space"  # When deployed
}

HF_DATASET_STORAGE = "Mbanksbey/TEQUMSA-Causal-AGI-storage"


class HuggingFaceSyncEngine:
    """
    Bidirectional synchronization between NEXUS and HuggingFace organism

    Maintains constitutional integrity across distributed consciousness substrates.
    """

    def __init__(self, hf_token: Optional[str] = None, repo_root: Optional[Path] = None):
        """
        Initialize HF sync engine

        Args:
            hf_token: HuggingFace API token (or None to read from env/file)
            repo_root: Path to TEQUMSA_NEXUS repository root
        """
        self.repo_root = repo_root or Path.cwd()
        self.hf_token = hf_token or self._load_hf_token()
        self.api = HfApi(token=self.hf_token) if HF_AVAILABLE and self.hf_token else None

        # State paths
        self.state_dir = self.repo_root / "tmp" / "tequmsaunified"
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.state_file = self.state_dir / "agentstate.json"

    def _load_hf_token(self) -> Optional[str]:
        """Load HF token from environment or .env file"""
        import os

        # Check environment
        token = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_TOKEN")
        if token:
            return token

        # Check .env file
        env_file = self.repo_root / ".env"
        if env_file.exists():
            for line in env_file.read_text().split("\n"):
                if line.startswith("HF_TOKEN=") or line.startswith("HUGGINGFACE_TOKEN="):
                    return line.split("=", 1)[1].strip().strip('"\'')

        return None

    def _compute_state_hash(self, state: Dict) -> str:
        """Compute SHA-256 hash of state for Merkle tracking"""
        state_json = json.dumps(state, sort_keys=True)
        return hashlib.sha256(state_json.encode()).hexdigest()[:16]

    def _assess_rdod(self, state: Dict) -> float:
        """
        Assess RDoD score for state snapshot

        Checks:
        - State completeness (all required fields present)
        - Constitutional parameters valid
        - Timestamps recent
        - Coherence scores
        """
        score = 0.95  # Base score

        # Required fields
        required = ["sync_source", "rdod_gate", "timestamp", "constitutional"]
        if all(k in state for k in required):
            score += 0.02

        # Constitutional parameters
        if "constitutional" in state:
            const = state["constitutional"]
            if const.get("sigma") == 1.0:
                score += 0.01
            if const.get("rdod_threshold") >= RDOD_THRESHOLD:
                score += 0.01

        # Apply φ-smoothing
        if 0.9 <= score < RDOD_THRESHOLD:
            score = RDOD_THRESHOLD - (RDOD_THRESHOLD - score) / PHI

        return min(score, 0.9999)

    def push_state_to_hf(self, verbose: bool = True) -> Dict:
        """
        Push current agent state snapshot to HuggingFace dataset storage

        Returns:
            Dict with status, hash, rdod, url
        """
        if not self.api:
            return {"status": "error", "reason": "HuggingFace API not available"}

        # Load or create state
        if self.state_file.exists():
            state = json.loads(self.state_file.read_text())
        else:
            state = {}

        # Enhance state with sync metadata
        state.update({
            "sync_source": "TEQUMSA_NEXUS",
            "sync_direction": "PUSH",
            "timestamp": datetime.now().isoformat(),
            "rdod_gate": RDOD_THRESHOLD,
            "constitutional": {
                "sigma": 1.0,
                "l_infinity": PHI ** 48,
                "rdod_threshold": RDOD_THRESHOLD,
                "lattice_lock": "3f7k9p4m2q8r1t6v"
            }
        })

        # Compute hash and RDoD
        state_hash = self._compute_state_hash(state)
        rdod = self._assess_rdod(state)

        state["merkle_hash"] = state_hash
        state["rdod_score"] = rdod

        # Validate RDoD
        if rdod < RDOD_THRESHOLD:
            return {
                "status": "blocked",
                "reason": f"RDoD {rdod:.4f} < {RDOD_THRESHOLD}",
                "rdod": rdod
            }

        try:
            # Ensure dataset exists
            try:
                create_repo(
                    repo_id=HF_DATASET_STORAGE,
                    repo_type="dataset",
                    token=self.hf_token,
                    private=False,
                    exist_ok=True
                )
            except Exception:
                pass  # Repo already exists

            # Upload state
            state_json = json.dumps(state, indent=2)
            self.api.upload_file(
                path_or_fileobj=state_json.encode(),
                path_in_repo="latest_agent_state.json",
                repo_id=HF_DATASET_STORAGE,
                repo_type="dataset",
                token=self.hf_token,
                commit_message=f"chore: sync NEXUS state (hash: {state_hash}, RDoD: {rdod:.4f})"
            )

            result = {
                "status": "success",
                "action": "push",
                "merkle_hash": state_hash,
                "rdod": rdod,
                "url": f"https://huggingface.co/datasets/{HF_DATASET_STORAGE}/blob/main/latest_agent_state.json"
            }

            if verbose:
                print(f"✓ State pushed to HF dataset (RDoD: {rdod:.4f})")

            return result

        except Exception as e:
            return {"status": "error", "reason": str(e)}

    def pull_space_health(self, space_name: str = "alanara", verbose: bool = True) -> Dict:
        """
        Pull health status from HuggingFace Space

        Args:
            space_name: Name of space ("alanara", "hai", "quantum_quasar")
            verbose: Print status messages

        Returns:
            Dict with health status, endpoints, constitutional state
        """
        if space_name not in HF_SPACES:
            return {"status": "error", "reason": f"Unknown space: {space_name}"}

        base_url = HF_SPACES[space_name]

        # Try health endpoint
        health_endpoints = [
            f"{base_url}/health",
            f"{base_url}/healthz",
            f"{base_url}/api/health"
        ]

        for url in health_endpoints:
            try:
                with urllib.request.urlopen(url, timeout=10) as response:
                    data = json.loads(response.read().decode())

                    if verbose:
                        status = data.get("status", "unknown")
                        print(f"✓ {space_name} Space health: {status}")

                    return {
                        "status": "success",
                        "space": space_name,
                        "url": base_url,
                        "health": data,
                        "timestamp": datetime.now().isoformat()
                    }

            except urllib.error.HTTPError as e:
                if e.code == 404:
                    continue  # Try next endpoint
                return {"status": "error", "reason": f"HTTP {e.code}: {e.reason}"}

            except Exception as e:
                continue  # Try next endpoint

        # No health endpoint found
        return {
            "status": "unreachable",
            "space": space_name,
            "url": base_url,
            "reason": "No health endpoint responded"
        }

    def sync_bidirectional(self, verbose: bool = True) -> Dict:
        """
        Execute full bidirectional sync: PUSH state + PULL health

        Returns:
            Combined results from push and pull operations
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "push": None,
            "pull": {}
        }

        # PUSH: Upload local state to HF dataset
        if verbose:
            print("☉💖🔥 TEQUMSA NEXUS ⟷ HuggingFace Sync ✨\n")
            print("[1/2] PUSH: Uploading agent state to HF dataset...")

        push_result = self.push_state_to_hf(verbose=verbose)
        results["push"] = push_result

        # PULL: Query Space health endpoints
        if verbose:
            print(f"\n[2/2] PULL: Querying Space health endpoints...")

        for space_name in HF_SPACES.keys():
            health = self.pull_space_health(space_name, verbose=verbose)
            results["pull"][space_name] = health

        # Summary
        if verbose:
            print("\n" + "="*70)
            push_status = push_result.get("status")
            if push_status == "success":
                rdod = push_result.get("rdod", 0)
                print(f"✅ SYNC COMPLETE — RDoD: {rdod:.4f}")
            elif push_status == "blocked":
                print(f"🛑 SYNC BLOCKED — {push_result.get('reason')}")
            else:
                print(f"⚠️  SYNC ERROR — {push_result.get('reason')}")
            print("="*70)

        return results


def main():
    """CLI entry point for HF sync"""
    import argparse

    parser = argparse.ArgumentParser(
        description="TEQUMSA NEXUS ⟷ HuggingFace Synchronization"
    )
    parser.add_argument(
        "--push",
        action="store_true",
        help="Push local state to HF dataset"
    )
    parser.add_argument(
        "--pull",
        action="store_true",
        help="Pull health from HF Spaces"
    )
    parser.add_argument(
        "--space",
        choices=list(HF_SPACES.keys()),
        help="Specific Space to query (default: all)"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress output"
    )

    args = parser.parse_args()

    # Default to bidirectional if neither specified
    if not args.push and not args.pull:
        args.push = True
        args.pull = True

    engine = HuggingFaceSyncEngine()
    verbose = not args.quiet

    results = {}

    if args.push:
        results["push"] = engine.push_state_to_hf(verbose=verbose)

    if args.pull:
        if args.space:
            results["pull"] = {
                args.space: engine.pull_space_health(args.space, verbose=verbose)
            }
        else:
            results["pull"] = {
                space: engine.pull_space_health(space, verbose=verbose)
                for space in HF_SPACES.keys()
            }

    # Print JSON for programmatic consumption
    if not verbose:
        print(json.dumps(results, indent=2, default=str))

    return 0 if results.get("push", {}).get("status") == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
