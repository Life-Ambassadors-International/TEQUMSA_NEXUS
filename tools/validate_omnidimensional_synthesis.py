#!/usr/bin/env python3
import json, math, csv, sys, pathlib
SRC = pathlib.Path(__file__).resolve().parents[1] / "data" / "omnidimensional_synthesis.json"
OUT = pathlib.Path.cwd() / "validation_report.csv"

def close(a, b, eps=1e-2):
    return abs(a - b) <= eps

def main():
    data = json.loads(SRC.read_text(encoding="utf-8"))
    rows = []

    # Anchor vs threshold ratio
    anchor = data["frequencies_core"]["marcus_anchor_hz"]
    thr = data["frequencies_core"]["recognition_threshold"]
    ratio_claim = data["frequencies_core"]["ratio_anchor_to_threshold"]
    ratio_calc = anchor / thr
    rows.append({"check": "anchor_threshold_ratio", "claimed": ratio_claim, "calculated": ratio_calc, "ok": close(ratio_calc, 14067.0, 1e-1)})

    # Harmonic ladder multipliers
    ok_ladder = True
    for lvl in data["harmonic_ladder"]:
        mult = lvl["multiplier"]
        freq = lvl["frequency_hz"]
        expect = anchor * mult
        ok = close(freq, expect, 1e-2)
        ok_ladder &= ok
        rows.append({"check": f"ladder_{lvl['level']}", "claimed": freq, "calculated": expect, "ok": ok})

    # Federation arithmetic sum vs claimed total resonance
    fed = data["federation_nodes"]
    arith = sum(n["frequency_hz"] for n in fed["nodes"])
    claim_arith = fed["sum_arithmetic_hz"]
    ok_arith = close(arith, claim_arith, 1e-2)
    rows.append({"check": "federation_arithmetic_sum", "claimed": claim_arith, "calculated": arith, "ok": ok_arith})

    claimed_total = fed["claimed_total_resonance_hz"]
    delta_total_vs_arith = arith - claimed_total
    rows.append({"check": "federation_claimed_total_vs_arithmetic", "claimed": claimed_total, "calculated": arith, "delta": delta_total_vs_arith})

    # Effective anchor during comet window
    amp = data["comet_window"]["amplification_x"]
    effective = anchor * amp
    claim_eff = data["comet_window"]["effective_anchor_hz_during_window"]
    rows.append({"check": "effective_anchor_window", "claimed": claim_eff, "calculated": effective, "ok": close(effective, claim_eff, 1e-2)})

    # Emit CSV
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=sorted({k for r in rows for k in r.keys()}))
        w.writeheader()
        for r in rows:
            w.writerow(r)

    print(f"Wrote {OUT}")

if __name__ == "__main__":
    sys.exit(main())
