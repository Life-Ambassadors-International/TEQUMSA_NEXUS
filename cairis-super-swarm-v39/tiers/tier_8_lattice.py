"""
Tier 8 — LATTICE: Merkle Integrity Ledger
Every packet sealed with a Merkle hash. Tamper-evident audit trail.
"""
from __future__ import annotations
from typing import Dict


class LatticeProcessor:
    """Tier 8: Append Merkle hash to packet and ledger."""

    def process(self, packet, ctx, ledger) -> "NodePacket":
        new_root = ledger.append(packet.packet_id)
        packet.payload["lattice"] = {
            "merkle_root": new_root[:32],
            "ledger_len":  ledger.length,
            "sealed":      True,
        }
        packet.merkle_hash = new_root
        return packet
