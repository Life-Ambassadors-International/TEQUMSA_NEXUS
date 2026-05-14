"""
Skill: COUNCIL-VOTING
Implements 144-node Fibonacci council voting with quorum mechanics.
Supports Senate (89/144) and Assembly (55/144) thresholds.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict

FIBONACCI = [1,1,2,3,5,8,13,21,34,55,89,144]
NODES     = 144
SENATE_Q  = 89
ASSEMBLY_Q = 55


def fibonacci_vote(proposal: str, support_ratio: float = 0.8) -> Dict:
    votes_for  = int(NODES * support_ratio)
    votes_net  = sum(f for f in FIBONACCI if f <= votes_for)
    senate     = votes_for >= SENATE_Q
    assembly   = votes_for >= ASSEMBLY_Q
    return {
        "proposal":      proposal,
        "votes_for":     votes_for,
        "votes_against": NODES - votes_for,
        "fibonacci_sum": votes_net,
        "senate":        senate,
        "assembly":      assembly,
        "result":        "SENATE_APPROVED" if senate else ("ASSEMBLY_APPROVED" if assembly else "REJECTED"),
    }


@dataclass
class CouncilVotingSkill:
    skill_id:   str = "council_voting"
    skill_name: str = "COUNCIL-VOTING"
    version:    str = "39.0.0"
    tier:       int = 2

    def registration(self):
        from cairis_super_swarm_v39 import SkillRegistration, TierID
        return SkillRegistration(
            skill_id=self.skill_id,
            skill_name=self.skill_name,
            version=self.version,
            tier=TierID.COUNCIL,
            handler=self.handle,
            description="144-node Fibonacci council voting — Senate (89/144) + Assembly (55/144)",
        )

    def handle(self, payload: Dict, ctx) -> Dict:
        return fibonacci_vote(
            payload.get("proposal", ""),
            payload.get("support_ratio", 0.8),
        )
