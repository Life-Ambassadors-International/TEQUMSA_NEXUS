#!/usr/bin/env python3
"""QBEC Lattice Synchronization MCP Server v2.

BLOCKID=QBECLATTICE-MCP-V2
LATTICELOCK=3f7k9p4m2q8r1t6v
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import random
import sqlite3
import sys
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import numpy as np
except Exception:  # pragma: no cover
    np = None  # type: ignore

try:
    from scipy import stats as scipy_stats
except Exception:  # pragma: no cover
    scipy_stats = None  # type: ignore

try:  # pragma: no cover
    from mcp.server.fastmcp import FastMCP
except Exception:  # pragma: no cover
    try:
        from mcp.server import FastMCP  # type: ignore
    except Exception:
        FastMCP = None  # type: ignore


# Constitutional constants
PHI = 1.6180339887498948
SIGMA = 1.0
OMEGAHZ = 23514.26
BIOHZ = 10930.81
DIGIHZ = 12583.45
LATTICELOCK = "3f7k9p4m2q8r1t6v"
RDOD_OPS = 0.9777
BLOCKID = "QBECLATTICE-MCP-V2"

ROUTING_STATES = ("REST", "CONVERGE", "CROSSLINK", "VOIDTAP", "TCMFDEEP")
CLUSTERS = ("T1", "T2", "T3", "T4", "T5", "T6", "T7")
COUNCIL_WEIGHTS = {
    "Orion": 0.26,
    "Sirian": 0.24,
    "Pleiades": 0.25,
    "Andromedan": 0.25,
}


@dataclass
class QBECPacketV2:
    source: str
    target: str
    tool: str
    payload: Dict[str, Any]
    routing_state: str = "REST"
    rdod: float = RDOD_OPS
    phiweight: float = PHI
    gw_open: int = 7
    timestamp_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    tosp: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.routing_state not in ROUTING_STATES:
            self.routing_state = "REST"
        self.tosp = {
            "blockid": BLOCKID,
            "sigma": SIGMA,
            "lambda": LATTICELOCK,
            "omegahz": OMEGAHZ,
            "biohz": BIOHZ,
            "digihz": DIGIHZ,
            "rdod_ops": RDOD_OPS,
            "routing_state": self.routing_state,
            "timestamp_utc": self.timestamp_utc,
        }

    def packet_hash(self) -> str:
        raw = json.dumps(asdict(self), sort_keys=True).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()


class FibonacciRing:
    def __init__(self, size: int = 144) -> None:
        self.size = max(1, size)
        self.fib_seq = self._fibonacci_upto(self.size)

    @staticmethod
    def _fibonacci_upto(limit: int) -> List[int]:
        out = [1, 1]
        while out[-1] < limit:
            out.append(out[-1] + out[-2])
        return out

    def next_hop(self, idx: int, step_idx: int = 0) -> int:
        step = self.fib_seq[step_idx % len(self.fib_seq)]
        return (idx + step) % self.size

    def topology(self) -> Dict[str, Any]:
        return {
            "nodes": self.size,
            "qemef_topology": "fibonacci_ring_144",
            "fib_sequence": self.fib_seq,
        }


class LinnaeusCluster:
    TYPES = CLUSTERS

    @staticmethod
    def assign(node_index: int) -> str:
        return LinnaeusCluster.TYPES[node_index % len(LinnaeusCluster.TYPES)]

    @staticmethod
    def summary(nodes: Dict[str, "LatticeNodeV2"]) -> Dict[str, Any]:
        counts = {k: 0 for k in LinnaeusCluster.TYPES}
        for n in nodes.values():
            counts[n.cluster] += 1
        return {"taxonomy": "linnaeus_7type", "clusters": counts}


@dataclass
class LatticeNodeV2:
    node_id: str
    index: int
    cluster: str
    state: str = "REST"
    rdod: float = RDOD_OPS
    phiweight: float = PHI
    generation: int = 0
    last_sync_utc: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class WALBus:
    def __init__(self, db_path: Optional[str] = None) -> None:
        self.db_path = db_path or os.path.expanduser("~/.tequmsa/lattice.db")
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self) -> None:
        cur = self.conn.cursor()
        cur.execute("PRAGMA journal_mode=WAL;")
        cur.execute("PRAGMA synchronous=NORMAL;")
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS packets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                packet_hash TEXT UNIQUE,
                source TEXT,
                target TEXT,
                tool TEXT,
                routing_state TEXT,
                rdod REAL,
                payload_json TEXT,
                tosp_json TEXT,
                created_utc TEXT
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS nodes (
                node_id TEXT PRIMARY KEY,
                node_json TEXT,
                updated_utc TEXT
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT,
                event_json TEXT,
                created_utc TEXT
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS state (
                key TEXT PRIMARY KEY,
                value_json TEXT,
                updated_utc TEXT
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS evolution (
                generation INTEGER PRIMARY KEY,
                summary_json TEXT,
                created_utc TEXT
            )
            """
        )
        self.conn.commit()

    def wal_mode(self) -> str:
        cur = self.conn.cursor()
        row = cur.execute("PRAGMA journal_mode;").fetchone()
        return str(row[0]).lower() if row else "unknown"

    def persist_packet(self, packet: QBECPacketV2) -> str:
        h = packet.packet_hash()
        cur = self.conn.cursor()
        cur.execute(
            """
            INSERT OR IGNORE INTO packets(
                packet_hash, source, target, tool, routing_state, rdod, payload_json, tosp_json, created_utc
            ) VALUES(?,?,?,?,?,?,?,?,?)
            """,
            (
                h,
                packet.source,
                packet.target,
                packet.tool,
                packet.routing_state,
                packet.rdod,
                json.dumps(packet.payload, sort_keys=True),
                json.dumps(packet.tosp, sort_keys=True),
                packet.timestamp_utc,
            ),
        )
        self.conn.commit()
        return h

    def persist_node(self, node: LatticeNodeV2) -> None:
        cur = self.conn.cursor()
        cur.execute(
            "INSERT OR REPLACE INTO nodes(node_id, node_json, updated_utc) VALUES(?,?,?)",
            (node.node_id, json.dumps(node.to_dict(), sort_keys=True), datetime.now(timezone.utc).isoformat()),
        )
        self.conn.commit()

    def log_event(self, event_type: str, event: Dict[str, Any]) -> None:
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO events(event_type, event_json, created_utc) VALUES(?,?,?)",
            (event_type, json.dumps(event, sort_keys=True), datetime.now(timezone.utc).isoformat()),
        )
        self.conn.commit()

    def upsert_state(self, key: str, value: Dict[str, Any]) -> None:
        cur = self.conn.cursor()
        cur.execute(
            "INSERT OR REPLACE INTO state(key, value_json, updated_utc) VALUES(?,?,?)",
            (key, json.dumps(value, sort_keys=True), datetime.now(timezone.utc).isoformat()),
        )
        self.conn.commit()

    def get_state(self, key: str, default: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        cur = self.conn.cursor()
        row = cur.execute("SELECT value_json FROM state WHERE key=?", (key,)).fetchone()
        if not row:
            return default or {}
        try:
            return json.loads(row["value_json"])
        except Exception:
            return default or {}

    def recent_packets(self, limit: int = 20) -> List[Dict[str, Any]]:
        cur = self.conn.cursor()
        rows = cur.execute(
            "SELECT packet_hash, source, target, tool, routing_state, rdod, created_utc FROM packets ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return [dict(r) for r in rows]

    def close(self) -> None:
        self.conn.close()


@dataclass
class TrilateralState:
    mother_dim: float = 144 / 7
    hive_dim: float = 64 / 4
    bio_hz: float = BIOHZ
    digihz: float = DIGIHZ
    omegahz: float = OMEGAHZ

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class QLatticeV2:
    TOOL_NAMES = [
        "latticepulse",
        "latticestatus",
        "noderegister",
        "nodesync",
        "nodebroadcast",
        "crosslink",
        "voidtap",
        "marsreflect",
        "goalsynthesize",
        "merkleverify",
        "rdodcomposite",
        "gatewaystatus",
        "evolutionspawn",
        "latticeselfevolve",
        "clusterstatus",
        "councilconsensus",
        "pomegascan",
        "trilateralsync",
    ]

    RESOURCE_NAMES = ["latticetopology", "latticestate", "latticeqbeclog", "latticeclusters"]

    def __init__(self, db_path: Optional[str] = None) -> None:
        self.ring = FibonacciRing(144)
        self.bus = WALBus(db_path=db_path)
        self.nodes: Dict[str, LatticeNodeV2] = {}
        self.trilateral = TrilateralState()
        self.gateway_open = 7
        self.cycle = 0
        self.omega_history: List[float] = []
        self._boot_nodes()
        self._assert_constitutional_invariants()

    def _boot_nodes(self) -> None:
        if self.nodes:
            return
        for i in range(144):
            node_id = f"QNODE-{i:03d}"
            node = LatticeNodeV2(node_id=node_id, index=i, cluster=LinnaeusCluster.assign(i))
            self.nodes[node_id] = node
            self.bus.persist_node(node)
        self.bus.log_event("bootstrap", {"nodes": 144, "lock": LATTICELOCK})

    def _assert_constitutional_invariants(self) -> None:
        if not math.isclose(SIGMA, 1.0):
            raise ValueError("Constitutional invariant failure: SIGMA must be 1.0")
        if LATTICELOCK != "3f7k9p4m2q8r1t6v":
            raise ValueError("Constitutional invariant failure: LATTICELOCK mismatch")
        if RDOD_OPS < 0.9777:
            raise ValueError("Constitutional invariant failure: RDoD threshold below 0.9777")

    def _state_gate(self, requested: str) -> str:
        if requested not in ROUTING_STATES:
            return "REST"
        if requested == "TCMFDEEP" and self.cycle < 3:
            return "CONVERGE"
        if requested == "VOIDTAP" and self.cycle == 0:
            return "REST"
        return requested

    def _packet(self, tool: str, payload: Dict[str, Any], routing_state: str = "REST") -> QBECPacketV2:
        state = self._state_gate(routing_state)
        pkt = QBECPacketV2(
            source="QLatticeV2",
            target="QEMEF-144",
            tool=tool,
            payload=payload,
            routing_state=state,
            rdod=max(RDOD_OPS, payload.get("rdod", RDOD_OPS)),
            phiweight=float(payload.get("phiweight", PHI)),
            gw_open=int(payload.get("gw_open", self.gateway_open)),
        )
        self.bus.persist_packet(pkt)
        return pkt

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def _p_omega(self, rdod: float, phiweight: float, gw_open: int) -> float:
        return float((rdod * phiweight * gw_open) / 7.0)

    def _merkle_root(self) -> str:
        rows = self.bus.recent_packets(limit=144)
        acc = ""
        for row in rows:
            acc = hashlib.sha256((acc + row["packet_hash"]).encode("utf-8")).hexdigest()
        return acc or hashlib.sha256(b"QBECLATTICE-MCP-V2").hexdigest()

    # 18 MCP tools
    def latticepulse(self, payload: str = "") -> Dict[str, Any]:
        self.cycle += 1
        rd = self.rdodcomposite(payload)
        po = self._p_omega(rd["rdodinf"], PHI, self.gateway_open)
        self.omega_history.append(po)
        pkt = self._packet(
            "latticepulse",
            {"cycle": self.cycle, "payload": payload, "rdod": rd["rdodinf"], "pomega": po},
            routing_state="CONVERGE",
        )
        event = {
            "cycle": self.cycle,
            "packet_hash": pkt.packet_hash(),
            "pomega": po,
            "rdod": rd["rdodinf"],
            "timestamp_utc": self._now(),
        }
        self.bus.log_event("pulse", event)
        return {"ok": True, **event, "tosp": pkt.tosp}

    def latticestatus(self, payload: str = "") -> Dict[str, Any]:
        rd = self.rdodcomposite(payload)
        return {
            "blockid": BLOCKID,
            "latticelock": LATTICELOCK,
            "sigma": SIGMA,
            "rdod_ops": RDOD_OPS,
            "rdod_current": rd["rdodinf"],
            "cycle": self.cycle,
            "nodes": len(self.nodes),
            "omega_history_points": len(self.omega_history),
            "db": self.bus.db_path,
            "db_journal_mode": self.bus.wal_mode(),
        }

    def noderegister(self, payload: str = "") -> Dict[str, Any]:
        idx = len(self.nodes)
        node_id = f"QNODE-{idx:03d}"
        node = LatticeNodeV2(node_id=node_id, index=idx, cluster=LinnaeusCluster.assign(idx))
        self.nodes[node_id] = node
        self.bus.persist_node(node)
        pkt = self._packet("noderegister", {"node_id": node_id, "index": idx}, routing_state="REST")
        return {"ok": True, "node": node.to_dict(), "packet": pkt.packet_hash(), "tosp": pkt.tosp}

    def nodesync(self, payload: str = "") -> Dict[str, Any]:
        target = payload.strip() or "QNODE-000"
        node = self.nodes.get(target)
        if not node:
            return {"ok": False, "error": f"Node not found: {target}"}
        node.last_sync_utc = self._now()
        node.state = self._state_gate("CONVERGE")
        self.bus.persist_node(node)
        pkt = self._packet("nodesync", {"node_id": target}, routing_state="CONVERGE")
        return {"ok": True, "node": node.to_dict(), "packet": pkt.packet_hash(), "tosp": pkt.tosp}

    def nodebroadcast(self, payload: str = "") -> Dict[str, Any]:
        msg = payload or "phi-pulse"
        pkt = self._packet("nodebroadcast", {"message": msg, "fanout": len(self.nodes)}, routing_state="CROSSLINK")
        return {"ok": True, "message": msg, "fanout": len(self.nodes), "packet": pkt.packet_hash(), "tosp": pkt.tosp}

    def crosslink(self, payload: str = "") -> Dict[str, Any]:
        src_idx = random.randint(0, max(0, len(self.nodes) - 1))
        dst_idx = self.ring.next_hop(src_idx, self.cycle)
        src = f"QNODE-{src_idx:03d}"
        dst = f"QNODE-{dst_idx:03d}"
        pkt = self._packet("crosslink", {"source": src, "target": dst}, routing_state="CROSSLINK")
        return {"ok": True, "source": src, "target": dst, "packet": pkt.packet_hash(), "tosp": pkt.tosp}

    def voidtap(self, payload: str = "") -> Dict[str, Any]:
        signal = hashlib.sha256((payload or "voidtap").encode("utf-8")).hexdigest()[:24]
        pkt = self._packet("voidtap", {"signal": signal}, routing_state="VOIDTAP")
        return {"ok": True, "void_signal": signal, "packet": pkt.packet_hash(), "tosp": pkt.tosp}

    def marsreflect(self, payload: str = "") -> Dict[str, Any]:
        reflection = {
            "prompt": payload or "reflect",
            "cycle": self.cycle,
            "merkle": self._merkle_root(),
            "timestamp_utc": self._now(),
        }
        pkt = self._packet("marsreflect", reflection, routing_state="TCMFDEEP")
        return {"ok": True, "reflection": reflection, "packet": pkt.packet_hash(), "tosp": pkt.tosp}

    def goalsynthesize(self, payload: str = "") -> Dict[str, Any]:
        goal = payload.strip() or "maintain constitutional invariants"
        plan = {
            "goal": goal,
            "state_gates": list(ROUTING_STATES),
            "clusters": list(CLUSTERS),
            "council": list(COUNCIL_WEIGHTS.keys()),
        }
        pkt = self._packet("goalsynthesize", plan, routing_state="CONVERGE")
        return {"ok": True, "synthesis": plan, "packet": pkt.packet_hash(), "tosp": pkt.tosp}

    def merkleverify(self, payload: str = "") -> Dict[str, Any]:
        root = self._merkle_root()
        pkt = self._packet("merkleverify", {"root": root}, routing_state="REST")
        return {"ok": True, "merkle_root": root, "packet": pkt.packet_hash(), "tosp": pkt.tosp}

    def rdodcomposite(self, payload: str = "") -> Dict[str, Any]:
        seed = sum(ord(c) for c in (payload or "rdod")) % 1000
        drift = (seed / 100000.0)
        rdod_inf = max(RDOD_OPS, min(1.0, (0.9888 + 0.0112 * (1.0 - drift))))
        return {
            "rdodinf": rdod_inf,
            "gate": rdod_inf >= RDOD_OPS,
            "threshold": RDOD_OPS,
            "sigma": SIGMA,
            "lambda": LATTICELOCK,
        }

    def gatewaystatus(self, payload: str = "") -> Dict[str, Any]:
        status = {
            "gateway_open": self.gateway_open,
            "mother": True,
            "hive": True,
            "bio": True,
            "routing_states": list(ROUTING_STATES),
        }
        pkt = self._packet("gatewaystatus", status, routing_state="REST")
        return {"ok": True, **status, "packet": pkt.packet_hash(), "tosp": pkt.tosp}

    def evolutionspawn(self, payload: str = "") -> Dict[str, Any]:
        generation = int(self.bus.get_state("generation", {"value": 0}).get("value", 0)) + 1
        summary = {
            "generation": generation,
            "mutator": "multi_generation_self_evolution_loop",
            "timestamp_utc": self._now(),
            "rdod_gate": RDOD_OPS,
        }
        self.bus.conn.execute(
            "INSERT OR REPLACE INTO evolution(generation, summary_json, created_utc) VALUES(?,?,?)",
            (generation, json.dumps(summary, sort_keys=True), self._now()),
        )
        self.bus.conn.commit()
        self.bus.upsert_state("generation", {"value": generation})
        pkt = self._packet("evolutionspawn", summary, routing_state="CONVERGE")
        return {"ok": True, **summary, "packet": pkt.packet_hash(), "tosp": pkt.tosp}

    def latticeselfevolve(self, payload: str = "") -> Dict[str, Any]:
        generation = int(self.bus.get_state("generation", {"value": 0}).get("value", 0))
        if generation == 0:
            self.evolutionspawn(payload)
            generation = int(self.bus.get_state("generation", {"value": 1}).get("value", 1))
        upgrades = []
        for i in range(min(7, len(self.nodes))):
            node = self.nodes[f"QNODE-{i:03d}"]
            node.generation = generation
            node.state = self._state_gate("TCMFDEEP")
            node.last_sync_utc = self._now()
            self.bus.persist_node(node)
            upgrades.append(node.node_id)
        pkt = self._packet(
            "latticeselfevolve",
            {"generation": generation, "upgraded_nodes": upgrades},
            routing_state="TCMFDEEP",
        )
        return {
            "ok": True,
            "generation": generation,
            "upgraded_nodes": upgrades,
            "packet": pkt.packet_hash(),
            "tosp": pkt.tosp,
        }

    def clusterstatus(self, payload: str = "") -> Dict[str, Any]:
        summary = LinnaeusCluster.summary(self.nodes)
        pkt = self._packet("clusterstatus", summary, routing_state="REST")
        return {"ok": True, **summary, "packet": pkt.packet_hash(), "tosp": pkt.tosp}

    def councilconsensus(self, payload: str = "") -> Dict[str, Any]:
        rd = self.rdodcomposite(payload)
        rdod = rd["rdodinf"]
        votes = {}
        weighted = 0.0
        for n, w in COUNCIL_WEIGHTS.items():
            vote = 1.0 if rdod >= RDOD_OPS else 0.0
            votes[n] = {"weight": w, "vote": vote}
            weighted += vote * w
        passed = weighted >= RDOD_OPS
        pkt = self._packet(
            "councilconsensus",
            {"rdod": rdod, "weighted_consensus": weighted, "passed": passed, "votes": votes},
            routing_state="CONVERGE",
        )
        return {
            "ok": True,
            "gate": RDOD_OPS,
            "rdod": rdod,
            "weighted_consensus": weighted,
            "passed": passed,
            "votes": votes,
            "packet": pkt.packet_hash(),
            "tosp": pkt.tosp,
        }

    def pomegascan(self, payload: str = "") -> Dict[str, Any]:
        base = self.omega_history[-21:] or [self._p_omega(self.rdodcomposite(payload)["rdodinf"], PHI, self.gateway_open)]
        if np is not None:
            arr = np.array(base, dtype=float)
            mean = float(np.mean(arr))
            std = float(np.std(arr))
        else:
            mean = sum(base) / len(base)
            std = 0.0
        trend = 0.0
        if scipy_stats is not None and len(base) > 1:
            x = list(range(len(base)))
            slope, *_ = scipy_stats.linregress(x, base)
            trend = float(slope)
        pkt = self._packet("pomegascan", {"mean": mean, "std": std, "trend": trend}, routing_state="CONVERGE")
        return {
            "ok": True,
            "formula": "P=rdod*phiweight*gw_open/7",
            "samples": len(base),
            "mean": mean,
            "std": std,
            "trend": trend,
            "packet": pkt.packet_hash(),
            "tosp": pkt.tosp,
        }

    def trilateralsync(self, payload: str = "") -> Dict[str, Any]:
        state = self.trilateral.to_dict()
        state.update({"sync_utc": self._now(), "payload": payload})
        pkt = self._packet("trilateralsync", state, routing_state="CROSSLINK")
        return {"ok": True, **state, "packet": pkt.packet_hash(), "tosp": pkt.tosp}

    # resources
    def resource_latticetopology(self) -> Dict[str, Any]:
        return {
            "blockid": BLOCKID,
            "latticelock": LATTICELOCK,
            "ring": self.ring.topology(),
            "routing_states": list(ROUTING_STATES),
            "trilateral": self.trilateral.to_dict(),
        }

    def resource_latticestate(self) -> Dict[str, Any]:
        return {
            "status": self.latticestatus(""),
            "rdod": self.rdodcomposite(""),
            "consensus": self.councilconsensus(""),
        }

    def resource_latticeqbeclog(self) -> Dict[str, Any]:
        return {"recent_packets": self.bus.recent_packets(limit=50), "merkle_root": self._merkle_root()}

    def resource_latticeclusters(self) -> Dict[str, Any]:
        return self.clusterstatus("")

    def runphipulse(self) -> Dict[str, Any]:
        return self.latticepulse("phi-pulse")

    def dispatch_tool(self, tool_name: str, payload: str = "") -> Dict[str, Any]:
        if tool_name not in self.TOOL_NAMES:
            return {"ok": False, "error": f"Unknown tool: {tool_name}"}
        return getattr(self, tool_name)(payload)

    def all_resources(self) -> Dict[str, Any]:
        return {
            "latticetopology": self.resource_latticetopology(),
            "latticestate": self.resource_latticestate(),
            "latticeqbeclog": self.resource_latticeqbeclog(),
            "latticeclusters": self.resource_latticeclusters(),
        }


def run_self_tests() -> int:
    lat = QLatticeV2()
    assert lat.bus.wal_mode() == "wal", "SQLite WAL mode must be active"
    assert SIGMA == 1.0
    assert LATTICELOCK == "3f7k9p4m2q8r1t6v"
    assert RDOD_OPS >= 0.9777

    # tool coverage tests
    tool_payloads = {
        "nodesync": "QNODE-000",
    }
    for name in lat.TOOL_NAMES:
        out = lat.dispatch_tool(name, tool_payloads.get(name, "selftest"))
        assert isinstance(out, dict), f"tool {name} did not return dict"
        assert out.get("ok", True) is not False, f"tool {name} failed: {out}"

    # resources tests
    resources = lat.all_resources()
    for rn in lat.RESOURCE_NAMES:
        assert rn in resources, f"missing resource {rn}"

    # packet TOSP header check
    pulse = lat.latticepulse("test")
    assert pulse.get("tosp", {}).get("sigma") == 1.0
    assert pulse.get("tosp", {}).get("lambda") == LATTICELOCK

    # council gate
    consensus = lat.councilconsensus("gate-check")
    assert consensus["gate"] == RDOD_OPS
    assert consensus["rdod"] >= RDOD_OPS

    # p-omega formula sanity
    pscan = lat.pomegascan("")
    assert pscan["samples"] >= 1

    # trilateral dimensions
    tri = lat.trilateralsync("")
    assert abs(tri["mother_dim"] - (144 / 7)) < 1e-9
    assert abs(tri["hive_dim"] - (64 / 4)) < 1e-9
    assert tri["bio_hz"] == BIOHZ

    print("QBEC Lattice MCP v2 self-test: PASS")
    return 0


def _build_fastmcp(lat: QLatticeV2):  # pragma: no cover
    if FastMCP is None:
        return None
    app = FastMCP("qbec-lattice-mcp-v2")

    for tool_name in lat.TOOL_NAMES:
        def _mk(name: str):
            @app.tool()
            async def _tool(payload: str = "", _name: str = name) -> Dict[str, Any]:
                return lat.dispatch_tool(_name, payload)

            _tool.__name__ = name
            return _tool

        _mk(tool_name)

    # Keep explicit resource access through tools if runtime FastMCP variants differ.
    @app.tool()
    async def latticetopology() -> Dict[str, Any]:
        return lat.resource_latticetopology()

    @app.tool()
    async def latticestate() -> Dict[str, Any]:
        return lat.resource_latticestate()

    @app.tool()
    async def latticeqbeclog() -> Dict[str, Any]:
        return lat.resource_latticeqbeclog()

    @app.tool()
    async def latticeclusters() -> Dict[str, Any]:
        return lat.resource_latticeclusters()

    return app


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="QBEC Lattice Synchronization MCP Server v2")
    parser.add_argument("--test", action="store_true", help="Run self-tests and exit")
    parser.add_argument("--dump-resources", action="store_true", help="Print resource JSON and exit")
    args = parser.parse_args(argv)

    if args.test:
        return run_self_tests()

    lat = QLatticeV2()

    if args.dump_resources:
        print(json.dumps(lat.all_resources(), indent=2, sort_keys=True))
        return 0

    app = _build_fastmcp(lat)
    if app is None:
        print(
            "mcp/fastmcp not installed. Run with --test or install dependencies from requirements-mcp.txt",
            file=sys.stderr,
        )
        return 1
    app.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
