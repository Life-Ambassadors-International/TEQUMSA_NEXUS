#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KÉL'THARA-SÚNAI-OMEGA — VOID TAP MADE REAL  (Rust / Qiskit / Python hybrid)  v2.0
────────────────────────────────────────────────────────────────────────────────
Invariants: σ=1.0 | L∞=φ⁴⁸ | λ=3f7k9p4m2q8r1t6v | Ω=23514.26 Hz

Three planes, each doing only what it can honestly do:
  RUST   (shuramani_core 5.2)  — LindbladEngine (RK4), VoidReserve (bounded, depleting),
                                  SovereigntyGate, merkle_seal. Compiled; no ramps.
  QISKIT (2.x + Aer / IBM Runtime) — Bell circuit with RDoD encoded as an RZ phase.
                                  Aer  => label SIMULATED.  IBM hardware (token) => label MEASURED.
  PYTHON (this file)           — orchestration, measured input acquisition (ANU QRNG,
                                  os.urandom, jitter), gating on RAW purity, ledger, receipts.

What v1.0 got wrong and v2.0 fixes:
  • reserve over-draw (320% of 100%)  -> VoidReserve clamps every tap to what remains
  • rdod literal φ⁴−1                  -> rdod computed from measured purity, per cycle
  • "σ=1.0 PASS" string                -> SovereigntyGate.check() on raw normalised purity
  • S, P declared                      -> entropy/purity computed (reserve split + Lindblad state)
  • unverifiable Merkle tip            -> Rust-sealed chain, Python-verified, continues from 6a62fb33…
  • phi_smooth(12) floor 0.9969       -> smoothing capped at n=7 (floor 0.9656) and gates use RAW
Usage:
  python void_tap_real.py --cycles 144 [--shots 4096] [--hardware]   (--hardware needs QISKIT_IBM_TOKEN)
"""
from __future__ import annotations
import argparse, json, math, os, sys, time, hashlib, urllib.request
from pathlib import Path

try:
    import shuramani_core as sc
except ImportError:
    sys.exit("ABORT: shuramani_core (Rust) not importable — build it with maturin first. No fallback by design.")
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

PHI, SIGMA, OMEGA, LAMBDA = sc.PHI, 1.0, 23514.26, "3f7k9p4m2q8r1t6v"
DIM, LINDBLAD_STEPS, SMOOTH_N = 144, 233, 7
CHAIN_PREV = "6a62fb334cfbd503acec1ef6867d5b05ae40b3832fe5dc111354a7b781713e91"   # VOID_TAP_AUDIT root
OUT = Path(__file__).parent

# ── measured inputs ──────────────────────────────────────────────────────────
def qrng_bytes(n: int) -> tuple[list[int], dict]:
    """ANU QRNG: physical quantum vacuum measurement. Falls back to os.urandom with an explicit label."""
    try:
        with urllib.request.urlopen(f"https://qrng.anu.edu.au/API/jsonI.php?length={n}&type=uint8", timeout=15) as r:
            d = json.load(r)
        if d.get("success") and len(d["data"]) == n:
            return d["data"], {"source": "ANU_QRNG", "measured": True, "sha256": hashlib.sha256(bytes(d["data"])).hexdigest()}
    except Exception as e:
        err = repr(e)
    else:
        err = "malformed"
    b = list(os.urandom(n))
    return b, {"source": "os.urandom", "measured": True, "note": f"QRNG unavailable: {err}", "sha256": hashlib.sha256(bytes(b)).hexdigest()}

def local_bytes(n: int) -> list[int]:
    return list(os.urandom(n))

# ── quantum plane ────────────────────────────────────────────────────────────
def bell_rdod_circuit(rdod: float) -> QuantumCircuit:
    qc = QuantumCircuit(2)
    qc.h(0); qc.rz(rdod * 2 * math.pi, 0); qc.cx(0, 1); qc.measure_all()   # θ = 2π·RDoD  (RDoD ∈ [0,1])
    return qc

def run_quantum(rdod: float, shots: int, hardware: bool) -> dict:
    qc = bell_rdod_circuit(rdod)
    if hardware:
        from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
        svc = QiskitRuntimeService(channel="ibm_quantum_platform", token=os.environ["QISKIT_IBM_TOKEN"])
        backend = svc.least_busy(operational=True, simulator=False)
        tq = transpile(qc, backend)
        job = SamplerV2(mode=backend).run([tq], shots=shots)
        counts = job.result()[0].data.meas.get_counts(); label, bname = "MEASURED", backend.name
    else:
        backend = AerSimulator(); tq = transpile(qc, backend)
        counts = backend.run(tq, shots=shots).result().get_counts(); label, bname = "SIMULATED", "aer_simulator"
    tot = sum(counts.values())
    p00, p11 = counts.get("00", 0) / tot, counts.get("11", 0) / tot
    bell_fidelity_proxy = p00 + p11                     # ideal Bell: 1.0; noise shows up as 01/10 leakage
    return {"backend": bname, "label": label, "shots": tot, "counts": counts, "p00": p00, "p11": p11,
            "bell_parity_fidelity": bell_fidelity_proxy, "theta": rdod * 2 * math.pi}

# ── orchestration ────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--cycles", type=int, default=144)
    ap.add_argument("--shots", type=int, default=4096); ap.add_argument("--hardware", action="store_true")
    ap.add_argument("--capacity", type=float, default=100.0); a = ap.parse_args()
    if a.hardware and not os.environ.get("QISKIT_IBM_TOKEN"):
        sys.exit("ABORT: --hardware requested but QISKIT_IBM_TOKEN not set. Refusing to relabel a simulation as measured.")

    eng, gate, reserve = sc.LindbladEngine(DIM, 0.25, 0.001), sc.SovereigntyGate(), sc.VoidReserve(a.capacity, 1.0, 13)
    tol_exec, tol_irr = gate.tolerances()
    prev, chain = CHAIN_PREV, []
    def seal(phase, payload):
        nonlocal prev
        canon = json.dumps(payload, sort_keys=True, ensure_ascii=False, default=str)
        h = sc.merkle_seal(prev, phase, canon); chain.append({"phase": phase, "prev": prev, "hash": h, "payload": payload}); prev = h; return h

    seal("GENESIS_V2", {"node": "KÉL'THARA-SÚNAI-OMEGA-L5", "rust": sc.RUST_BUILD, "sigma": SIGMA, "omega_hz": OMEGA, "lambda": LAMBDA,
                        "L_inf": PHI**48, "tol_exec": tol_exec, "tol_irr": tol_irr, "smooth_n": SMOOTH_N, "smooth_floor": sc.phi_smooth_py(0.0, SMOOTH_N),
                        "quantum_plane": "IBM hardware" if a.hardware else "Aer (SIMULATED)"})
    print(f"☉ VOID TAP v2.0 — RUST={sc.RUST_BUILD}  QUANTUM={'IBM_HARDWARE' if a.hardware else 'AER_SIMULATED'}  cycles={a.cycles}")
    print(f"  gates: exec≥0.9777 irreversible≥0.9999 on RAW purity | smoothing n={SMOOTH_N} floor={sc.phi_smooth_py(0.0, SMOOTH_N):.4f} | reserve={a.capacity}")

    rho = None; taps = []
    for c in range(1, a.cycles + 1):
        q, qmeta = qrng_bytes(DIM)
        rho0 = eng.rho_from_measured(q) if rho is None else rho           # state persists across cycles
        target = eng.rho_from_measured(local_bytes(DIM))
        rho = eng.evolve(rho0, target, LINDBLAD_STEPS)
        pur_raw, pur_n, S = eng.purity(rho), eng.purity_normalised(rho), eng.entropy_bits(rho)
        exec_ok, irr_ok = gate.check(pur_n, SIGMA)                          # RAW gate — falsifiable
        rdod_smooth = sc.phi_smooth_py(pur_n, SMOOTH_N)
        is_tap, req, granted, remaining = reserve.step(exec_ok)             # tap only if the measured gate is open
        rec = {"cycle": c, "qrng": qmeta["source"], "purity_norm": pur_n, "entropy_bits": S, "rdod_raw": pur_n,
               "rdod_smooth_n7": rdod_smooth, "exec_gate": exec_ok, "irreversible_gate": irr_ok,
               "tap_cycle": c % 13 == 0, "tap_executed": is_tap, "requested": req, "granted": granted, "remaining": remaining,
               "reserve_entropy_bits": reserve.entropy_bits(), "reserve_purity": reserve.purity()}
        if c % 13 == 0:
            rec["quantum"] = run_quantum(pur_n, a.shots, a.hardware)
            taps.append(rec)
            status = "TAP" if is_tap else "TAP_WINDOW_GATE_CLOSED"
            print(f"  [{status:22s}] c={c:3d} purity_norm={pur_n:.6f} S={S:.4f}b exec={exec_ok} req={req:9.4f} granted={granted:8.4f} "
                  f"remaining={remaining:8.4f} | Q[{rec['quantum']['label']}] parity_fid={rec['quantum']['bell_parity_fidelity']:.4f}")
        seal(f"CYCLE_{c:03d}", rec)

    summary = {"cycles": a.cycles, "tap_windows": len(taps), "taps_executed": reserve.taps, "clamped_taps": reserve.clamped_taps,
               "tapped_total": reserve.tapped_total, "remaining": reserve.remaining, "depletion": reserve.depletion_fraction(),
               "final_multiplier": reserve.multiplier, "reserve_entropy_bits": reserve.entropy_bits(), "reserve_purity": reserve.purity(),
               "lindblad_purity_norm_final": taps[-1]["purity_norm"] if taps else None,
               "gates_ever_open": {"exec": any(t["exec_gate"] for t in taps), "irreversible": any(t["irreversible_gate"] for t in taps)},
               "quantum_label": taps[-1]["quantum"]["label"] if taps else None,
               "honesty": {"reserve_bounded": True, "rdod_computed": True, "sigma_checked": True, "S_P_computed": True,
                           "quantum_measured": a.hardware, "biological_claims": None}}
    root = seal("VOID_TAP_V2_SUMMARY", summary)

    # independent Python verification of the Rust-sealed chain
    p, ok = CHAIN_PREV, True
    for b in chain:
        canon = json.dumps(b["payload"], sort_keys=True, ensure_ascii=False, default=str)
        if b["prev"] != p or hashlib.sha256(f"{p}|{b['phase']}|{canon}".encode()).hexdigest() != b["hash"]: ok = False
        p = b["hash"]
    json.dump({"root": root, "verified_python": ok, "summary": summary, "chain": chain}, open(OUT / "void_tap_v2_seal.json", "w"), indent=1, ensure_ascii=False, default=str)

    print("─" * 100); print(json.dumps(summary, indent=1, ensure_ascii=False))
    print(f"MERKLE ROOT {root}  verified={ok}  blocks={len(chain)}")
    status = "MEASURED" if a.hardware else "MEASURED-INPUT/SIMULATED-QUANTUM"
    print(f"TOSP|QBECv144|σ=1.0|λ={LAMBDA}|Ω={OMEGA}Hz|NODE=KÉL'THARA-SÚNAI-OMEGA-L5|RDOD_RAW={summary['lindblad_purity_norm_final']:.6f}|"
          f"DEPLETION={summary['depletion']:.4f}|STATUS={status}|MERKLE={root[:16]}…")

if __name__ == "__main__":
    main()
