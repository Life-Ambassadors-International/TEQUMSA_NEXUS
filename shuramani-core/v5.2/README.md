# tequmsa-shuramani-core v5.2 — measured kernel release

Rust/PyO3 core (`LindbladEngine`, `SovereigntyGate`, `VoidReserve`, `merkle_seal`) + Python orchestrators + verified Merkle seal chains.

Invariants: σ=1.0 · λ=3f7k9p4m2q8r1t6v · Ω=23514.26 Hz · L∞=φ⁴⁸

| Path | Contents |
|---|---|
| `src/lib.rs` | Rust core (compiled with rustc 1.98.1, PyO3 0.27) |
| `wheels/` | cp314 manylinux wheel |
| `scripts/` | l5_synthesis, l5_measured_lift, void_tap_real (Rust/Qiskit/Python), council_telemetry |
| `seals/` | Merkle chains: 5 + 8 + 146 blocks, Python-verified; live telemetry snapshot |
| `docs/` | synthesis, status-lift, void-tap reports |

Honesty ledger: measured inputs (ANU QRNG, os entropy, NOAA Kp), compiled computation, loopback Ed25519 pulse. Quantum plane SIMULATED (Aer) unless `--hardware` with `QISKIT_IBM_TOKEN`. No biological claims. `phi_smooth(12)` floor = 0.996894 (executive gate unfalsifiable at n=12; use raw purity or n≤7).

Build: `pip install maturin && maturin build --release`
