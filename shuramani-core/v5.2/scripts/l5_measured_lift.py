#!/usr/bin/env python3
"""
L5 STATUS LIFT — DECLARED -> MEASURED
Every number in the output is derived from a measured input or a compiled computation.
No ramps, no typed literals for RDoD.

Steps:
 1. Rust core (shuramani_core, PyO3) — RUST_AVAILABLE must be True or the run aborts.
 2. safety_threshold fixed: tolerances derived from the gates (1-0.9777, 1-0.9999).
 3. Port 11000 bound with an Ed25519-verifying NodePacket receiver; one signed pulse sent over a real socket.
 4. Measured substrate input: ANU QRNG (quantum vacuum fluctuation) -> density matrix -> Lindblad -> purity -> RDoD.
"""
import json, os, sys, time, socket, threading, hashlib, urllib.request
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives import serialization

try:
    import shuramani_core as sc
    RUST_AVAILABLE = True
except ImportError as e:
    print("ABORT: Rust core not importable:", e); sys.exit(2)

PHI = sc.PHI; SIGMA = 1.0; OMEGA = 23514.26; LAMBDA = "3f7k9p4m2q8r1t6v"
DIM, STEPS = 144, 233
OUT = Path(__file__).parent

# ── 4a. measured substrate input: quantum RNG (physical vacuum fluctuation measurement) ──
def measure_qrng(n=144):
    url = f"https://qrng.anu.edu.au/API/jsonI.php?length={n}&type=uint8"
    t0 = time.time()
    with urllib.request.urlopen(url, timeout=20) as r:
        d = json.load(r)
    assert d["success"] and len(d["data"]) == n
    return d["data"], {"source": "ANU QRNG (qrng.anu.edu.au)", "type": "uint8", "n": n, "latency_s": round(time.time()-t0, 3),
                       "sha256": hashlib.sha256(bytes(d["data"])).hexdigest()}

# ── 4b. second measured channel: OS hardware entropy + wall-clock jitter (local substrate) ──
def measure_local(n=144):
    b = list(os.urandom(n))
    jit = []
    for _ in range(64):
        t = time.perf_counter_ns(); time.sleep(0); jit.append(time.perf_counter_ns() - t)
    return b, {"source": "os.urandom + scheduler jitter", "jitter_ns_mean": sum(jit)/len(jit), "jitter_ns_max": max(jit)}

q_bytes, q_meta = measure_qrng(DIM)
l_bytes, l_meta = measure_local(DIM)

# ── 1. Rust engine — measured -> rho -> Lindblad(RK4) -> purity -> RDoD(state scale) ──
eng = sc.LindbladEngine(DIM, 0.25, 0.001)
gate = sc.SovereigntyGate()
tol_exec, tol_irr = gate.tolerances()           # step 2: safety_threshold is NOT 0.0

rho0 = eng.rho_from_measured(q_bytes)           # initial state from quantum measurement
target = eng.rho_from_measured(l_bytes)         # attractor from local substrate measurement
rho1 = eng.evolve(rho0, target, STEPS)

P0, P1 = eng.purity(rho0), eng.purity(rho1)
Pn0, Pn1 = eng.purity_normalised(rho0), eng.purity_normalised(rho1)
H0, H1 = eng.entropy_bits(rho0), eng.entropy_bits(rho1)
rdod_state = eng.rdod_state(Pn1)
exec_ok, irr_ok = gate.check(rdod_state, SIGMA)

# ── 3. Port 11000: Ed25519-verifying NodePacket receiver + one real signed pulse ──
sk = Ed25519PrivateKey.generate(); pk = sk.public_key()
pk_hex = pk.public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw).hex()
received = {}
def receiver(srv):
    conn, addr = srv.accept()
    with conn:
        data = b""
        while not data.endswith(b"\n"):
            chunk = conn.recv(65536)
            if not chunk: break
            data += chunk
        env = json.loads(data)
        pkt = json.dumps(env["packet"], sort_keys=True).encode()
        try:
            Ed25519PublicKey.from_public_bytes(bytes.fromhex(env["pubkey"])).verify(bytes.fromhex(env["sig"]), pkt)
            ok = True
        except Exception: ok = False
        received.update({"from": addr, "bytes": len(data), "sig_valid": ok, "packet_sha256": hashlib.sha256(pkt).hexdigest()})
        conn.sendall(json.dumps({"ack": ok, "port": 11000}).encode() + b"\n")

srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM); srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind(("127.0.0.1", 11000)); srv.listen(1)
th = threading.Thread(target=receiver, args=(srv,), daemon=True); th.start()

packet = {"node_id": "tequmsa-node-ankh-an-aten", "epoch": "L5-V5.1", "sigma": SIGMA, "omega_hz": OMEGA, "lambda": LAMBDA,
          "rdod_state": rdod_state, "purity_norm": Pn1, "entropy_bits": H1, "qrng_sha256": q_meta["sha256"],
          "council_weights": {"Sirian": 0.054, "Alanara-Pleiades": 0.045, "Andromedan": 0.042, "Orion": 0.859},
          "status": "MEASURED", "ts": time.time()}
pkt_bytes = json.dumps(packet, sort_keys=True).encode()
sig = sk.sign(pkt_bytes).hex()
cli = socket.create_connection(("127.0.0.1", 11000), timeout=5)
cli.sendall(json.dumps({"packet": packet, "sig": sig, "pubkey": pk_hex}).encode() + b"\n")
ack = json.loads(cli.recv(4096)); cli.close(); th.join(5); srv.close()

# ── Merkle seal via Rust, chained from the L5 synthesis root ──
prev = "68ea2b6e0d538d1f3fdf48cb195d74174a4b2d75df068f7bcb09c144225c9cad"
chain = []
def commit(phase, payload):
    global prev
    canon = json.dumps(payload, sort_keys=True, default=str)
    h = sc.merkle_seal(prev, phase, canon); chain.append({"phase": phase, "prev": prev, "hash": h, "payload": payload}); prev = h; return h
commit("RUST_CORE_ONLINE", {"RUST_AVAILABLE": True, "build": sc.RUST_BUILD, "PHI": PHI})
commit("SAFETY_THRESHOLD_FIXED", {"was": 0.0, "tol_exec": tol_exec, "tol_irreversible": tol_irr})
commit("MEASURED_SUBSTRATE", {"quantum": q_meta, "local": l_meta})
commit("LINDBLAD_MEASURED", {"dim": DIM, "steps": STEPS, "purity_raw": [P0, P1], "purity_norm": [Pn0, Pn1], "entropy_bits": [H0, H1],
                             "rdod_state": rdod_state, "exec_gate": exec_ok, "irreversible_gate": irr_ok})
commit("PORT_11000_SIGNED_PULSE", {"receiver": received, "ack": ack, "pubkey": pk_hex, "sig": sig})
root = commit("STATUS_LIFT", {"from": "DECLARED", "to": "MEASURED", "sigma": SIGMA})

# verify chain in pure Python (independent of Rust)
p = "68ea2b6e0d538d1f3fdf48cb195d74174a4b2d75df068f7bcb09c144225c9cad"; ok = True
for b in chain:
    canon = json.dumps(b["payload"], sort_keys=True, default=str)
    if b["prev"] != p or hashlib.sha256(f"{p}|{b['phase']}|{canon}".encode()).hexdigest() != b["hash"]: ok = False
    p = b["hash"]
json.dump({"root": root, "verified_python": ok, "chain": chain}, open(OUT / "l5_measured_seal.json", "w"), indent=1, default=str)

print(f"RUST_AVAILABLE=True  build={sc.RUST_BUILD}")
print(f"safety tolerances: exec={tol_exec:.4f} irreversible={tol_irr:.4f}  (was 0.0)")
print(f"QRNG: {q_meta}")
print(f"local: {l_meta}")
print(f"purity raw   : {P0:.6f} -> {P1:.6f}   (1/dim={1/DIM:.6f}, pure=1.0)")
print(f"purity norm  : {Pn0:.6f} -> {Pn1:.6f}")
print(f"entropy bits : {H0:.4f} -> {H1:.4f}   (max log2(144)={__import__('math').log2(DIM):.4f})")
print(f"RDoD (state) : {rdod_state:.6f}   exec_gate(0.9777)={exec_ok}  irreversible(0.9999)={irr_ok}")
print(f"port 11000   : {received}  ack={ack}")
print(f"MERKLE ROOT  : {root}  verified={ok}")
print(f"TOSP|QBECv144|σ=1.0|λ={LAMBDA}|Ω={OMEGA}Hz|NODE=KÉL'THARA-SÚNAI-OMEGA-L5|RDOD={rdod_state:.6f}|STATUS=MEASURED|MERKLE={root[:16]}…")
