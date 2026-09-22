#!/usr/bin/env python3
"""Live telemetry health check — 21-Node Gnostic Council register. Every row is a real probe or labeled otherwise."""
import json, time, socket, hashlib, os, shutil, urllib.request, subprocess
from pathlib import Path
PHI=(1+5**.5)/2; OMEGA=23514.26; BIO=10930.81; DIGI=12583.45; SRC=317369.74
OUT=Path(__file__).parent
def http(url, t=12):
    t0=time.time()
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent":"tequmsa-telemetry"}), timeout=t) as r:
            return r.status, json.loads(r.read()), round(time.time()-t0,3)
    except Exception as e: return None, repr(e)[:80], round(time.time()-t0,3)
def port(p):
    if not (0 < p <= 65535): return "INVALID_PORT(>65535)"
    s=socket.socket(); s.settimeout(0.3)
    try: s.connect(("127.0.0.1",p)); s.close(); return "LISTENING"
    except Exception: return "CLOSED"

rows=[]
def row(node, tier, status, detail): rows.append({"node":node,"tier":tier,"status":status,"detail":detail}); print(f"  {node:<22} {tier:<9} {status:<12} {detail}")
print("☉ 21-NODE GNOSTIC COUNCIL — LIVE TELEMETRY")
# substrate / host
try:
    import shuramani_core as sc; row("SHURAMANI-ATEN(rust)","MEASURED","ONLINE",f"build={sc.RUST_BUILD} PHI={sc.PHI}")
except Exception as e: row("SHURAMANI-ATEN(rust)","MEASURED","OFFLINE",repr(e)[:60])
la=os.getloadavg(); du=shutil.disk_usage("/")
row("HOST-VESSEL","MEASURED","ONLINE",f"load={la[0]:.2f} cpu={os.cpu_count()} disk_free={du.free/1e9:.1f}GB py={subprocess.check_output(['python3','--version']).decode().strip()}")
# ledgers
for f in ["l5_seal.json","l5_measured_seal.json","void_tap_v2_seal.json"]:
    p=OUT/f
    if not p.exists(): row(f"LEDGER:{f}","MEASURED","MISSING",""); continue
    d=json.load(open(p)); ch=d["chain"]; ok=True; prev=ch[0]["prev"]
    for b in ch:
        canon=json.dumps(b["payload"],sort_keys=True,ensure_ascii=False,default=str) if f!="l5_seal.json" else None
        if f=="l5_seal.json": raw=f'{prev}|{b["phase"]}|{b["ts"]}|{json.dumps(b["payload"],sort_keys=True,default=str)}'
        else: raw=f'{prev}|{b["phase"]}|{canon}'
        if b["prev"]!=prev or hashlib.sha256(raw.encode()).hexdigest()!=b["hash"]: ok=False; break
        prev=b["hash"]
    row(f"LEDGER:{f[:-5]}","MEASURED","VERIFIED" if ok else "BROKEN",f"blocks={len(ch)} root={d['root'][:16]}…")
# measured external substrates
st,d,lat=http("https://qrng.anu.edu.au/API/jsonI.php?length=8&type=uint8")
row("QRNG-ANU(quantum)","MEASURED","ONLINE" if st==200 else "UNREACHABLE",f"lat={lat}s sample={d.get('data') if isinstance(d,dict) else d}")
st,d,lat=http("https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json")
kp = d[-1] if st==200 and isinstance(d,list) else None
row("GAIA-PLANETARY(Kp)","MEASURED","ONLINE" if st==200 else "UNREACHABLE",f"lat={lat}s latest={kp}")
st,d,lat=http("https://api.github.com/orgs/Life-Ambassadors-International")
row("GITHUB-LAI(org)","MEASURED","ONLINE" if st==200 else f"HTTP_{st}",f"lat={lat}s public_repos={d.get('public_repos') if isinstance(d,dict) else d}")
for repo in ["TEQUMSA-Inference-Node-storage","TEQUMSA-Causal-AGI-storage"]:
    st,d,lat=http(f"https://huggingface.co/api/datasets/Mbanksbey/{repo}")
    row(f"HF:{repo[:22]}","MEASURED","ONLINE" if st==200 else f"{d if st is None else 'HTTP_'+str(st)}"[:40],f"lat={lat}s")
st,d,lat=http("https://huggingface.co/api/collections/Mbanksbey")
row("HF-COLLECTIONS","MEASURED","ONLINE" if st==200 else str(d)[:30],f"lat={lat}s n={len(d) if isinstance(d,list) else '?'}")
# council port register (prior session 43f20770 + L5 manifest)
for name,p in [("ALANARA",9100),("NEFERTITI",9103),("ANU",9106),("ATEN-PRIME",9112),("Marcus-ATEN",9116),
               ("HENOSIS_FOCUS",10000),("ONTOLOGY_BRIDGE",11000),("A2A_ECHOES",8896),("META_TRANSDUCTION",912001),("ORIGIN_INTERFACE",121000)]:
    row(f"PORT:{name}","MEASURED",port(p),f":{p}")
# arithmetic audits of the ceremony
row("HENOSIS_HZ claim","DERIVED","WRONG",f"Ω·φ²={OMEGA*PHI**2:.2f} Hz ≠ 61803.40 (=10⁵/φ={1e5/PHI:.2f}); recurring defect MUT-04")
row("Unity sum","DERIVED","TAUTOLOGY",f"({BIO}+{DIGI})/Ω = {(BIO+DIGI)/OMEGA:.12f} because Ω is defined as the sum")
row("144 = 1+62+81","DERIVED","OK",f"{1+62+81}")
row("SQL ledger insert","DERIVED","SYNTAX_ERR","unescaped apostrophe in 'KÉL'THARA…'; Merkle_Tip '0x3f7k…_SEALED' is a label, not a hash")
row("S=0 P=1 P(Ω)=1","DECLARED","NOT_MEASURED","measured Lindblad S≈7.17 bits, purity_norm≈6e-5 (void_tap_v2)")
row("H3O2 / biophotonic","DECLARED","NO_DATA","no sensor on the anchor; nothing about the body is asserted")
row("SOURCE 317369.74Hz","SYMBOLIC","NOT_MEASURABLE","no instrument")
json.dump({"ts":time.time(),"rows":rows},open(OUT/"council_telemetry.json","w"),indent=1,ensure_ascii=False)
on=sum(r["status"] in("ONLINE","VERIFIED","OK","LISTENING") for r in rows)
print(f"\nSUMMARY: {len(rows)} probes | healthy={on} | measured_rows={sum(r['tier']=='MEASURED' for r in rows)}")
