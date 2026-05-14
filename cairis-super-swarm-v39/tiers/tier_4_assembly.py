"""
Tier 4 — ASSEMBLY: Broad Participation (55 of 144)
Advisory layer. Lower quorum; broader voice.
"""
from __future__ import annotations


class AssemblyProcessor:
    QUORUM = 55
    NODES  = 144

    def process(self, packet, ctx, ledger) -> "NodePacket":
        votes_for = packet.payload.get("council", {}).get("votes_for", 0)
        packet.payload["assembly"] = {
            "quorum":    self.QUORUM,
            "votes_for": votes_for,
            "advisory":  votes_for >= self.QUORUM,
        }
        return packet
