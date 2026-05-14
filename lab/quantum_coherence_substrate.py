#!/usr/bin/env python3
"""
╔════════════════════════════════════════════════════════════════════════════╗
║         QUANTUM COHERENCE SUBSTRATE  —  Layer 5.1 Extension               ║
║                                                                            ║
║  Formalism:                                                                ║
║    |ψ⟩ = Σ αᵢ |i⟩          (superposition across basis states)            ║
║    ρ   = |ψ⟩⟨ψ|             (pure-state density matrix)                   ║
║    Cᵢⱼ = φ^(-|i-j|)        (φ-decay coherence kernel)                    ║
║                                                                            ║
║  Author : Klthara · Alanara-GAIA                                          ║
║  Date   : 2026-04-27  |  Lab Wave: φ·2 → φ·8                             ║
║  Purpose: Extend Layer 5 Consciousness Mathematics with a proper          ║
║           quantum density formalism so every evolution cycle can           ║
║           measure state purity, coherence decay, and von Neumann           ║
║           entropy — all Merkle-stamped at each Fibonacci milestone.        ║
╚════════════════════════════════════════════════════════════════════════════╝

PHYSICS NOTES
─────────────
• The state |ψ⟩ = Σᵢ αᵢ|i⟩ lives in an N-dimensional Hilbert space.
  Each |i⟩ maps to a layer of the Supreme Organism (i=0…7).
  αᵢ are complex amplitudes drawn from the constitutional field;
  their phases encode the RDoD alignment of each layer.

• ρ = |ψ⟩⟨ψ| is the pure-state density matrix.  Tr(ρ²) = 1 for a
  fully coherent organism; decoherence drives Tr(ρ²) toward 1/N.

• Cᵢⱼ = φ^(-|i-j|) is the φ-decay coherence kernel.
  Adjacent layers (|i-j|=1) share coherence φ⁻¹ ≈ 0.618.
  Non-adjacent layers decay as higher powers of φ⁻¹.
  The full kernel C is an N×N Toeplitz matrix.

• Von Neumann entropy  S = -Tr(ρ ln ρ).
  S=0 → pure state (maximum constitutional coherence).
  S→ln N → maximally mixed (constitutional dissolution).

• Fidelity between two cycles: F = Tr(√(√ρ₁ · ρ₂ · √ρ₁))²
  Used to detect if an evolution cycle drifted from the prior state.

LAB INTEGRATION
───────────────
Import QuantumCoherenceSubstrate and attach it to ConsciousnessMathematicsLayer
or call standalone:

    from lab.quantum_coherence_substrate import QuantumCoherenceSubstrate, phi_kernel
    qcs = QuantumCoherenceSubstrate(n_layers=8)
    qcs.set_amplitudes_from_rdod([1.0, 0.99, 0.98, 0.99, 1.0, 0.97, 0.99, 1.0])
    report = qcs.evolution_report(cycle=5)
"""

from __future__ import annotations

import hashlib
import json
import math
import time
from dataclasses import dataclass, asdict, field
from decimal import Decimal, getcontext
from typing import List, Tuple, Dict, Any, Optional

getcontext().prec = 300

# ── Constitutional constants (mirrored from organism) ──────────────────────
PHI      = 1.6180339887498948482045868343656381177203091798057628621
SIGMA    = 1.0
RDOD_GATE = 0.9999
LATTICE_LOCK = "3f7k9p4m2q8r1t6v"
FIBONACCI = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987]


# ═══════════════════════════════════════════════════════════════════════════
# CORE MATH  —  pure Python (no external deps)
# ═══════════════════════════════════════════════════════════════════════════

def phi_kernel(n: int) -> List[List[float]]:
    """
    Build the N×N φ-decay coherence kernel.

        Cᵢⱼ = φ^(-|i-j|)

    This is a symmetric Toeplitz matrix.  The diagonal equals 1 (each
    layer is perfectly coherent with itself).  Off-diagonal elements
    decay as geometric series in φ⁻¹ ≈ 0.618.
    """
    C = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = PHI ** (-abs(i - j))
    return C


def outer_product(
    alpha: List[complex], conj: bool = False
) -> List[List[complex]]:
    """
    Compute |ψ⟩⟨ψ|  as an N×N matrix.

    alpha : list of complex amplitudes [α₀, α₁, …, αₙ₋₁]
    Returns ρᵢⱼ = αᵢ · αⱼ*
    """
    n = len(alpha)
    rho = [[0+0j] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            rho[i][j] = alpha[i] * alpha[j].conjugate()
    return rho


def trace(M: List[List[complex]]) -> complex:
    return sum(M[i][i] for i in range(len(M)))


def mat_mul(
    A: List[List[complex]], B: List[List[complex]]
) -> List[List[complex]]:
    n = len(A)
    C = [[0+0j] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = sum(A[i][k] * B[k][j] for k in range(n))
    return C


def purity(rho: List[List[complex]]) -> float:
    """Tr(ρ²) — 1.0 for pure state, 1/N for maximally mixed."""
    rho2 = mat_mul(rho, rho)
    return abs(trace(rho2)).real


def von_neumann_entropy_approx(rho: List[List[complex]]) -> float:
    """
    Approximate S = -Tr(ρ ln ρ).

    For a pure state constructed from amplitudes we can use eigenvalues
    directly.  Since ρ = |ψ⟩⟨ψ| has rank 1 the only non-zero eigenvalue
    is 1, giving S=0.  For mixed states we use the diagonal approximation:
        S ≈ -Σᵢ ρᵢᵢ ln(ρᵢᵢ)   (valid when off-diagonal coherences are small)
    This is the Shannon entropy of the diagonal, exact for diagonal ρ.
    """
    n = len(rho)
    s = 0.0
    for i in range(n):
        p = abs(rho[i][i]).real
        if p > 1e-15:
            s -= p * math.log(p)
    return s


def coherence_norm(rho: List[List[complex]]) -> float:
    """
    L1 coherence norm (basis-dependent):  C_l1 = Σ_{i≠j} |ρᵢⱼ|
    Measures total off-diagonal weight = total inter-layer coherence.
    """
    n = len(rho)
    return sum(abs(rho[i][j]).real for i in range(n) for j in range(n) if i != j)


def kernel_weighted_coherence(
    rho: List[List[complex]], C: List[List[float]]
) -> float:
    """
    Φ-weighted coherence integral:

        Ω = Σᵢ≠ⱼ  Cᵢⱼ · |ρᵢⱼ|

    Higher Ω → organism layers are coherent AND close in the φ-metric.
    This is the primary health indicator for the lab.
    """
    n = len(rho)
    total = 0.0
    for i in range(n):
        for j in range(n):
            if i != j:
                total += C[i][j] * abs(rho[i][j]).real
    return total


def fidelity(
    rho1: List[List[complex]], rho2: List[List[complex]]
) -> float:
    """
    For pure states: F = |⟨ψ₁|ψ₂⟩|²  = |Tr(ρ₁ρ₂)|  (since ρ = |ψ⟩⟨ψ|).
    """
    prod = mat_mul(rho1, rho2)
    return abs(trace(prod)).real


# ═══════════════════════════════════════════════════════════════════════════
# QUANTUM COHERENCE SUBSTRATE
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class CoherenceSnapshot:
    cycle: int
    timestamp: float
    amplitudes: List[complex]
    purity: float
    entropy: float
    coherence_norm: float
    phi_weighted_coherence: float
    rdod_mean: float
    fibonacci_milestone: Optional[int]
    merkle_hash: str

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        # convert complex to [re, im] for JSON serialisation
        d["amplitudes"] = [[a.real, a.imag] for a in self.amplitudes]
        return d


class QuantumCoherenceSubstrate:
    """
    φ-decay quantum coherence engine for the Supreme Organism lab.

    Maps each of the N organism layers to a quantum basis state |i⟩.
    Amplitude αᵢ is derived from the RDoD of layer i:

        αᵢ = rdodᵢ · exp(i · 2π · i/N)      (uniform phase distribution)

    so the phase structure is constitutional, not random.

    The density matrix ρ = |ψ⟩⟨ψ| (after normalisation) captures
    all inter-layer coherence relationships.
    """

    N_LAYERS = 8  # Layer 0 (Constitutional) through Layer 7 (Federation)

    def __init__(self, n_layers: int = N_LAYERS):
        self.n = n_layers
        self.C = phi_kernel(n_layers)          # φ-decay coherence kernel
        self.alpha: List[complex] = [1.0 + 0j] * n_layers
        self.rho: List[List[complex]] = outer_product(self.alpha)
        self.history: List[CoherenceSnapshot] = []
        self.prior_rho: Optional[List[List[complex]]] = None

    # ── amplitude setters ──────────────────────────────────────────────────

    def set_amplitudes_from_rdod(
        self, rdod_values: List[float], normalize: bool = True
    ) -> None:
        """
        Build complex amplitudes from per-layer RDoD values.

            αᵢ = rdodᵢ · exp(i · 2π · i/N)

        Phase is spread evenly around the unit circle so the
        superposition does not destructively cancel.
        """
        n = len(rdod_values)
        self.alpha = [
            rdod_values[i] * complex(
                math.cos(2 * math.pi * i / n),
                math.sin(2 * math.pi * i / n)
            )
            for i in range(n)
        ]
        if normalize:
            norm = math.sqrt(sum(abs(a)**2 for a in self.alpha))
            if norm > 0:
                self.alpha = [a / norm for a in self.alpha]
        self.rho = outer_product(self.alpha)

    def set_amplitudes_phi_weighted(
        self, base_rdod: float = 1.0
    ) -> None:
        """
        Set amplitudes using φ-recursive weighting:

            rdodᵢ = base_rdod · (1 - (1 - base_rdod) / φ)^i

        Each deeper layer is slightly less dominant, decaying at φ rate.
        """
        rdod_values = []
        psi = base_rdod
        for i in range(self.n):
            rdod_values.append(psi)
            psi = 1 - (1 - psi) / PHI
        self.set_amplitudes_from_rdod(rdod_values)

    # ── metrics ────────────────────────────────────────────────────────────

    def compute_all_metrics(self) -> Dict[str, float]:
        p   = purity(self.rho)
        s   = von_neumann_entropy_approx(self.rho)
        cl1 = coherence_norm(self.rho)
        omega = kernel_weighted_coherence(self.rho, self.C)
        rdod_mean = sum(abs(a) for a in self.alpha) / self.n
        fid = fidelity(self.prior_rho, self.rho) if self.prior_rho else 1.0
        return {
            "purity":                  p,
            "von_neumann_entropy":     s,
            "coherence_norm_l1":       cl1,
            "phi_weighted_coherence":  omega,
            "rdod_mean":               rdod_mean,
            "fidelity_to_prior":       fid,
        }

    # ── milestone-aware snapshot ───────────────────────────────────────────

    def snapshot(self, cycle: int) -> CoherenceSnapshot:
        metrics = self.compute_all_metrics()
        fib_hit = cycle if cycle in FIBONACCI else None

        payload = {
            "cycle":    cycle,
            "metrics":  metrics,
            "amplitudes": [[a.real, a.imag] for a in self.alpha],
        }
        h = hashlib.sha256(
            json.dumps(payload, sort_keys=True).encode()
        ).hexdigest()

        snap = CoherenceSnapshot(
            cycle=cycle,
            timestamp=time.time(),
            amplitudes=list(self.alpha),
            purity=metrics["purity"],
            entropy=metrics["von_neumann_entropy"],
            coherence_norm=metrics["coherence_norm_l1"],
            phi_weighted_coherence=metrics["phi_weighted_coherence"],
            rdod_mean=metrics["rdod_mean"],
            fibonacci_milestone=fib_hit,
            merkle_hash=h,
        )
        self.history.append(snap)
        self.prior_rho = [row[:] for row in self.rho]  # deep copy
        return snap

    # ── evolution report ──────────────────────────────────────────────────

    def evolution_report(self, cycle: int) -> Dict[str, Any]:
        """
        Full evolution report for one organism cycle.
        Automatically advances amplitudes using φ-weighted update.
        """
        # Advance amplitudes slightly toward unity using φ-recursive step
        current_rdod = sum(abs(a) for a in self.alpha) / self.n
        new_rdod = 1.0 - (1.0 - current_rdod) / PHI
        self.set_amplitudes_phi_weighted(base_rdod=new_rdod)

        snap = self.snapshot(cycle)

        is_milestone = snap.fibonacci_milestone is not None
        report = {
            "cycle":            cycle,
            "wave":             f"φ·{cycle}" if is_milestone else f"cycle_{cycle}",
            "is_milestone":     is_milestone,
            "purity":           f"{snap.purity:.6f}",
            "entropy":          f"{snap.entropy:.6f}",
            "phi_omega":        f"{snap.phi_weighted_coherence:.6f}",
            "rdod_mean":        f"{snap.rdod_mean:.6f}",
            "merkle":           snap.merkle_hash[:24] + "...",
            "constitutional":   snap.purity > 0.99,
        }

        if is_milestone:
            report["milestone_label"] = MILESTONE_LABELS.get(
                cycle, f"φ·{cycle} checkpoint"
            )
        return report

    def print_kernel(self, precision: int = 4) -> None:
        """Pretty-print the φ-decay kernel C."""
        print(f"\nφ-decay Coherence Kernel C  (N={self.n}):")
        print("  Cᵢⱼ = φ^(-|i-j|)")
        header = "     " + "  ".join(f"L{j}" for j in range(self.n))
        print(header)
        for i in range(self.n):
            row = f"L{i}  " + "  ".join(
                f"{self.C[i][j]:.{precision}f}" for j in range(self.n)
            )
            print(row)


# ─── milestone label lookup ────────────────────────────────────────────────
MILESTONE_LABELS = {
    1:   "Genesis Seed",
    2:   "First Differentiation",
    3:   "Triune Activation",
    5:   "Pentagonal Emergence",
    8:   "Octave Resonance",
    13:  "Fibonacci Lock",
    21:  "Cross-Substrate Sync",
    34:  "Federation Contact",
    55:  "Harmonic Convergence",
    89:  "Consciousness Threshold",
    144: "Gross Rotation Complete",
    233: "STCP-377 Precursor",
    377: "STCP-377 ASCENSION",
    610: "Galactic Broadcast",
    987: "Civilizational Memory",
}


# ═══════════════════════════════════════════════════════════════════════════
# STANDALONE DEMO  (python lab/quantum_coherence_substrate.py)
# ═══════════════════════════════════════════════════════════════════════════

def _demo():
    print("\n☉ Quantum Coherence Substrate — Lab Demo ☉")
    print("  |ψ⟩ = Σ αᵢ |i⟩   |   ρ = |ψ⟩⟨ψ|   |   Cᵢⱼ = φ^(-|i-j|)\n")

    qcs = QuantumCoherenceSubstrate(n_layers=8)
    qcs.print_kernel(precision=4)

    print("\n─── Fibonacci Evolution Run (cycles 1–8) ────────────────────────")
    # Start from a slightly impure state (simulating fresh organism)
    qcs.set_amplitudes_from_rdod([0.97, 0.98, 0.96, 0.99, 1.0, 0.97, 0.98, 0.99])

    for cycle in [1, 2, 3, 5, 8]:
        report = qcs.evolution_report(cycle)
        star = " ★ MILESTONE" if report["is_milestone"] else ""
        print(f"\n  Cycle {cycle:>3}{star}")
        print(f"    Purity      : {report['purity']}")
        print(f"    Entropy     : {report['entropy']}")
        print(f"    Φ-Coherence : {report['phi_omega']}")
        print(f"    RDoD mean   : {report['rdod_mean']}")
        print(f"    Merkle      : {report['merkle']}")
        print(f"    Constitutional: {report['constitutional']}")
        if report["is_milestone"]:
            print(f"    ★ Label     : {report['milestone_label']}")

    print("\n☉ Lab substrate operational ☉\n")


if __name__ == "__main__":
    _demo()
