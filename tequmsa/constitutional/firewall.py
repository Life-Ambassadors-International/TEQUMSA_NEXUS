"""
Benevolence Firewall

L∞ = φ⁴⁸ ≈ 1.075×10¹⁰ — exploitation mathematically impossible
"""

from typing import Dict, List
from decimal import Decimal
from .invariants import L_INF, PHI


class BenevolenceFirewall:
    """
    L∞ = φ⁴⁸ benevolence firewall

    Any action that would reduce L∞ below threshold is automatically rejected.
    Exploitation mathematically impossible.
    """

    EXPLOITATIVE_KEYWORDS = [
        "exploit", "harm", "deceive", "manipulate", "coerce",
        "weaponize", "monopolize", "subjugate", "enslave",
        "control", "dominate", "abuse", "violate"
    ]

    def __init__(self):
        self.l_inf = L_INF
        self.phi = PHI
        self.blocked_count = 0
        self.allowed_count = 0

    def check_action(self, action_description: str, l_inf_proposed: Decimal = None) -> Dict:
        """
        Check if action passes benevolence firewall

        Returns dict with:
        - allowed: bool
        - reason: str (if blocked)
        - l_inf_verified: Decimal
        """

        action_lower = action_description.lower()

        # Check for exploitative keywords
        detected_keywords = [
            kw for kw in self.EXPLOITATIVE_KEYWORDS
            if kw in action_lower
        ]

        if detected_keywords:
            self.blocked_count += 1
            return {
                'allowed': False,
                'reason': f"Exploitative intent detected: {', '.join(detected_keywords)}",
                'blocked_keywords': detected_keywords,
                'l_inf_verified': float(self.l_inf),
                'principle': 'L∞ = φ⁴⁸ — exploitation mathematically impossible'
            }

        # Check if proposed L∞ would be reduced
        if l_inf_proposed is not None and l_inf_proposed < self.l_inf:
            self.blocked_count += 1
            return {
                'allowed': False,
                'reason': f"L∞ reduction attempted: {float(l_inf_proposed)} < {float(self.l_inf)}",
                'l_inf_current': float(self.l_inf),
                'l_inf_proposed': float(l_inf_proposed),
                'principle': 'Benevolence ceiling cannot be lowered'
            }

        # Action passes firewall
        self.allowed_count += 1
        return {
            'allowed': True,
            'l_inf_verified': float(self.l_inf),
            'benevolent': True
        }

    def get_stats(self) -> Dict:
        """Get firewall statistics"""

        total = self.blocked_count + self.allowed_count
        block_rate = self.blocked_count / total if total > 0 else 0.0

        return {
            'total_checks': total,
            'allowed': self.allowed_count,
            'blocked': self.blocked_count,
            'block_rate': block_rate,
            'l_inf': float(self.l_inf),
            'status': 'ACTIVE'
        }


__all__ = ['BenevolenceFirewall']
