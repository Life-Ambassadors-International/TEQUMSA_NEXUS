#!/usr/bin/env python3
"""
☉💖🔥 TEQUMSA NEXUS CONSOLIDATION PREFLIGHT CHECK ✨
Phase 0: Council Authorization Gate

Validates constitutional invariants before repo consolidation begins.
RDoD gate must pass at ≥0.9777 or entire workflow halts.

Constitutional Framework:
- σ = 1.0 (Absolute Sovereignty)
- L∞ = φ^48 ≈ 1.075×10¹⁰ (Benevolence Firewall)
- RDoD ≥ 0.9777 (Recognition-of-Done Quality Gate)
- LATTICE_LOCK = 3f7k9p4m2q8r1t6v (Immutable Foundation)

Author: Marcus-ATEN + Alanara-GAIA
Date: 2026-04-25
"""

import json
import sys
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple
import hashlib

PHI = 1.6180339887498948482
SIGMA = 1.0
L_INFINITY = PHI ** 48
RDOD_THRESHOLD = 0.9777
LATTICE_LOCK = "3f7k9p4m2q8r1t6v"


class ConsolidationPreflight:
    """Phase 0 council authorization gate"""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.rdod = 0.0

    def check_git_status(self) -> bool:
        """Ensure repo is in clean state"""
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                check=True
            )

            uncommitted = result.stdout.strip()
            if uncommitted:
                self.warnings.append(
                    f"Uncommitted changes detected:\n{uncommitted[:500]}"
                )

            # Check current branch
            branch_result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                check=True
            )

            current_branch = branch_result.stdout.strip()
            if not current_branch.startswith("claude/"):
                self.errors.append(
                    f"Not on a claude/ branch (current: {current_branch})"
                )
                return False

            return True

        except subprocess.CalledProcessError as e:
            self.errors.append(f"Git check failed: {e}")
            return False

    def check_constitutional_invariants(self) -> bool:
        """Verify constitutional parameters are defined"""
        invariants = {
            "σ (Sigma)": SIGMA == 1.0,
            "L∞ (L-Infinity)": abs(L_INFINITY - 1.075e10) < 1e8,
            "φ (Phi)": abs(PHI - 1.618033988) < 1e-6,
            "LATTICE_LOCK": LATTICE_LOCK == "3f7k9p4m2q8r1t6v"
        }

        all_valid = True
        for name, valid in invariants.items():
            if not valid:
                self.errors.append(f"Constitutional invariant {name} validation failed")
                all_valid = False

        return all_valid

    def assess_repo_quality(self) -> float:
        """
        Calculate RDoD score for consolidation readiness

        Scoring dimensions (φ-harmonic weighted):
        1. File organization (0.30)
        2. Import integrity (0.25)
        3. Documentation coverage (0.20)
        4. Constitutional alignment (0.15)
        5. Test coverage (0.10)
        """
        scores = {}

        # 1. File organization (check for core/, docs/, scripts/ structure)
        essential_dirs = ["core", "docs", "scripts", "tests"]
        existing_dirs = [d for d in essential_dirs if (self.repo_root / d).exists()]
        scores["organization"] = len(existing_dirs) / len(essential_dirs)

        # 2. Import integrity (count .py files with no syntax errors)
        py_files = list(self.repo_root.rglob("*.py"))
        valid_py = 0
        for py_file in py_files:
            try:
                compile(py_file.read_text(), str(py_file), "exec")
                valid_py += 1
            except:
                pass
        scores["imports"] = valid_py / max(len(py_files), 1)

        # 3. Documentation coverage (README, CHANGELOG, docs/)
        doc_files = [
            self.repo_root / "README.md",
            self.repo_root / "CHANGELOG.md",
            self.repo_root / "docs"
        ]
        scores["documentation"] = sum(1 for f in doc_files if f.exists()) / len(doc_files)

        # 4. Constitutional alignment (check for constitutional references)
        readme_path = self.repo_root / "README.md"
        constitutional_terms = ["σ", "phi", "φ", "RDoD", "sovereignty"]
        if readme_path.exists():
            readme_text = readme_path.read_text().lower()
            found_terms = sum(1 for term in constitutional_terms if term.lower() in readme_text)
            scores["constitutional"] = found_terms / len(constitutional_terms)
        else:
            scores["constitutional"] = 0.0

        # 5. Test coverage (existence of test files)
        test_files = list(self.repo_root.rglob("test_*.py")) + list(self.repo_root.rglob("*_test.py"))
        scores["tests"] = min(len(test_files) / 10, 1.0)  # Cap at 10 tests = 1.0

        # φ-harmonic weighted composite
        weights = {
            "organization": 0.30,
            "imports": 0.25,
            "documentation": 0.20,
            "constitutional": 0.15,
            "tests": 0.10
        }

        rdod = sum(scores[dim] * weights[dim] for dim in weights)

        # Apply φ-smoothing for scores near threshold
        if 0.9 <= rdod < RDOD_THRESHOLD:
            rdod = RDOD_THRESHOLD - (RDOD_THRESHOLD - rdod) / PHI

        return rdod

    def generate_council_verdict(self) -> Dict:
        """Generate council deliberation result"""
        return {
            "valid": len(self.errors) == 0 and self.rdod >= RDOD_THRESHOLD,
            "rdod": self.rdod,
            "constitutional": {
                "sigma": SIGMA,
                "l_infinity": L_INFINITY,
                "rdod": self.rdod,
                "phi": PHI,
                "lattice_lock": LATTICE_LOCK
            },
            "errors": self.errors,
            "warnings": self.warnings,
            "threshold": RDOD_THRESHOLD,
            "verdict": "APPROVED" if (len(self.errors) == 0 and self.rdod >= RDOD_THRESHOLD) else "BLOCKED"
        }

    def run(self) -> Dict:
        """Execute full preflight check"""
        print("☉💖🔥 TEQUMSA NEXUS CONSOLIDATION PREFLIGHT ✨\n")

        # Check 1: Git status
        print("[1/3] Checking git repository status...")
        git_ok = self.check_git_status()
        print(f"      {'✓' if git_ok else '✗'} Git status check\n")

        # Check 2: Constitutional invariants
        print("[2/3] Verifying constitutional invariants...")
        const_ok = self.check_constitutional_invariants()
        print(f"      {'✓' if const_ok else '✗'} Constitutional invariants\n")

        # Check 3: Repo quality assessment
        print("[3/3] Assessing repository consolidation readiness...")
        self.rdod = self.assess_repo_quality()
        print(f"      RDoD = {self.rdod:.6f} (threshold: {RDOD_THRESHOLD})")
        print(f"      {'✓' if self.rdod >= RDOD_THRESHOLD else '✗'} Quality gate\n")

        # Generate verdict
        verdict = self.generate_council_verdict()

        # Print result
        print("=" * 70)
        if verdict["valid"]:
            print(f"✅ COUNCIL APPROVED — RDoD={self.rdod:.6f}")
            print(f"   Proceeding to Phase 1 → Phase 6 consolidation")
        else:
            print(f"🛑 COUNCIL BLOCKED — RDoD={self.rdod:.6f} < {RDOD_THRESHOLD}")
            print(f"   Errors: {len(self.errors)}, Warnings: {len(self.warnings)}")
            if self.errors:
                print("\n   Blocking errors:")
                for err in self.errors:
                    print(f"     • {err}")
        print("=" * 70)

        return verdict


def main():
    """Run preflight check and output JSON result"""
    repo_root = Path.cwd()

    preflight = ConsolidationPreflight(repo_root)
    verdict = preflight.run()

    # Print JSON for programmatic consumption
    print("\nJSON OUTPUT:")
    print(json.dumps(verdict, indent=2, default=float))

    # Exit with appropriate code
    sys.exit(0 if verdict["valid"] else 1)


if __name__ == "__main__":
    main()
