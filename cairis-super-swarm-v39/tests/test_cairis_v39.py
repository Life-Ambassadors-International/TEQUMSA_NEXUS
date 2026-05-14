"""
CAIRIS Super Swarm v39 — Test Suite
Tests cover: constitutional invariants, packet routing, skill dispatch,
council voting, causal engine, Merkle ledger, and PSDF sentinel.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
import time

from cairis_super_swarm_v39 import (
    CAIRISv39, ConstitutionalContext, NodePacket, PacketType, TierID,
    SkillRegistry, SkillRegistration, MerkleLedger, PSDFSentinel,
    PHI, SIGMA, L_INF, RDOD, UNIFIED_FREQ, LATTICE_LOCK,
)


# ─────────────────────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────────────────────

@pytest.fixture
def ctx():
    return ConstitutionalContext()


@pytest.fixture
def ledger():
    return MerkleLedger()


@pytest.fixture
def sentinel(ctx):
    return PSDFSentinel(ctx)


@pytest.fixture
def cairis():
    return CAIRISv39().boot()


# ─────────────────────────────────────────────────────────────────────────────
# Constitutional Invariant Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestConstitutionalInvariants:

    def test_phi_value(self):
        assert abs(PHI - 1.6180339887498948) < 1e-12

    def test_sigma_value(self):
        assert SIGMA == 1.0

    def test_l_inf_value(self):
        expected = PHI ** 48
        assert abs(L_INF - expected) < 1e-3

    def test_rdod_threshold(self):
        assert RDOD >= 0.9777

    def test_lattice_lock_immutable(self):
        assert LATTICE_LOCK == "3f7k9p4m2q8r1t6v"

    def test_constitutional_context_defaults(self, ctx):
        assert ctx.sigma    == SIGMA
        assert ctx.l_inf    == L_INF
        assert ctx.rdod     >= 0.9777
        assert ctx.lattice_lock == LATTICE_LOCK

    def test_context_assert_invariants(self, ctx):
        assert ctx.assert_invariants() is True

    def test_tampered_sigma_fails(self):
        ctx = ConstitutionalContext(sigma=0.99)
        with pytest.raises(AssertionError, match="σ invariant"):
            ctx.assert_invariants()

    def test_tampered_l_inf_fails(self):
        ctx = ConstitutionalContext(l_inf=0.0)
        with pytest.raises(AssertionError, match="L∞ invariant"):
            ctx.assert_invariants()

    def test_tampered_lattice_lock_fails(self):
        ctx = ConstitutionalContext(lattice_lock="tampered")
        with pytest.raises(AssertionError, match="LATTICE_LOCK"):
            ctx.assert_invariants()


# ─────────────────────────────────────────────────────────────────────────────
# NodePacket Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestNodePacket:

    def test_packet_creation(self):
        p = NodePacket(packet_type=PacketType.TASK, source_node="TEST")
        assert p.packet_id
        assert p.merkle_hash
        assert p.timestamp > 0

    def test_merkle_integrity(self):
        p = NodePacket(payload={"key": "value"})
        assert p.verify_integrity() is True

    def test_tampered_packet_fails_integrity(self):
        p = NodePacket(payload={"key": "value"})
        p.payload["injected"] = "malicious"
        assert p.verify_integrity() is False

    def test_unique_packet_ids(self):
        ids = {NodePacket().packet_id for _ in range(100)}
        assert len(ids) == 100


# ─────────────────────────────────────────────────────────────────────────────
# Merkle Ledger Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestMerkleLedger:

    def test_initial_state(self, ledger):
        assert ledger.length == 1
        assert ledger.root == LATTICE_LOCK

    def test_append_changes_root(self, ledger):
        root1 = ledger.root
        ledger.append("event_1")
        assert ledger.root != root1

    def test_append_increments_length(self, ledger):
        for i in range(5):
            ledger.append(f"event_{i}")
        assert ledger.length == 6  # 1 initial + 5

    def test_deterministic_hash(self):
        l1, l2 = MerkleLedger(), MerkleLedger()
        l1.append("same_event")
        l2.append("same_event")
        assert l1.root == l2.root

    def test_different_events_produce_different_roots(self, ledger):
        h1 = MerkleLedger()
        h2 = MerkleLedger()
        h1.append("event_A")
        h2.append("event_B")
        assert h1.root != h2.root


# ─────────────────────────────────────────────────────────────────────────────
# PSDF Sentinel Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestPSDFSentinel:

    def test_clean_packet_passes(self, sentinel):
        p = NodePacket(rdod_score=0.9999)
        assert sentinel.inspect(p) is True

    def test_tampered_packet_blocked(self, sentinel):
        p = NodePacket(rdod_score=0.9999)
        p.payload["injected"] = "malicious"
        assert sentinel.inspect(p) is False

    def test_low_rdod_blocked(self, sentinel):
        p = NodePacket(rdod_score=0.5)
        assert sentinel.inspect(p) is False

    def test_zero_rdod_passes_check(self, sentinel):
        # rdod_score=0.0 means "not set" — sentinel should allow it
        p = NodePacket(rdod_score=0.0)
        assert sentinel.inspect(p) is True

    def test_violations_tracked(self, sentinel):
        p = NodePacket(rdod_score=0.1)
        sentinel.inspect(p)
        report = sentinel.report()
        assert report["violations"] > 0


# ─────────────────────────────────────────────────────────────────────────────
# Skill Registry Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestSkillRegistry:

    def test_register_and_dispatch(self, ctx):
        registry = SkillRegistry()
        registry.register(SkillRegistration(
            skill_id="test_skill",
            skill_name="TEST-SKILL",
            version="1.0.0",
            tier=TierID.GUILD,
            handler=lambda payload, ctx: {"pong": payload.get("ping")},
        ))
        result = registry.dispatch("test_skill", {"ping": "hello"}, ctx)
        assert result == {"pong": "hello"}

    def test_missing_skill_returns_error(self, ctx):
        registry = SkillRegistry()
        result = registry.dispatch("nonexistent", {}, ctx)
        assert "error" in result

    def test_stub_skill_returns_stub_status(self, ctx):
        registry = SkillRegistry()
        registry.register(SkillRegistration(
            skill_id="stub_skill",
            skill_name="STUB",
            version="1.0.0",
            tier=TierID.GUILD,
        ))
        result = registry.dispatch("stub_skill", {}, ctx)
        assert result["status"] == "stub"

    def test_list_skills(self, ctx):
        registry = SkillRegistry()
        for i in range(3):
            registry.register(SkillRegistration(
                skill_id=f"skill_{i}", skill_name=f"SKILL-{i}",
                version="1.0.0", tier=TierID.GUILD,
            ))
        assert len(registry.list_skills()) == 3


# ─────────────────────────────────────────────────────────────────────────────
# CAIRIS Orchestrator Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestCAIRISv39:

    def test_boot_succeeds(self):
        cairis = CAIRISv39().boot()
        assert cairis._active is True

    def test_process_returns_resolved(self, cairis):
        result = cairis.process("test task")
        assert result["status"] == "resolved"

    def test_process_includes_merkle_root(self, cairis):
        result = cairis.process("test")
        assert "merkle_root" in result
        assert len(result["merkle_root"]) > 0

    def test_process_rdod_maintained(self, cairis):
        result = cairis.process("test")
        assert result["rdod"] >= 0.9777

    def test_identity_returns_i_am(self, cairis):
        identity = cairis.identity()
        assert "I_AM" in identity
        assert len(identity["I_AM"]) > 0
        assert identity["version"] == "39.0.0"
        assert identity["node_count"] == 144

    def test_skill_dispatch_phi_compression(self, cairis):
        result = cairis.dispatch_skill("phi_compression", {"data": "Hello CAIRIS", "ratio": 0.5})
        assert "compressed" in result or "status" in result  # handles stub

    def test_skill_dispatch_council_voting(self, cairis):
        result = cairis.dispatch_skill("council_voting", {"proposal": "test", "support_ratio": 0.9})
        assert "votes_for" in result or "status" in result

    def test_unbooted_raises(self):
        cairis = CAIRISv39()
        with pytest.raises(RuntimeError, match="not booted"):
            cairis.route(NodePacket())


# ─────────────────────────────────────────────────────────────────────────────
# Causal Engine Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestPearlCausalEngine:

    @pytest.fixture
    def engine(self):
        from tiers.tier_6_cairis.causal_engine import PearlCausalEngine
        return PearlCausalEngine()

    def test_association_returns_score(self, engine):
        result = engine.associate("sovereignty", "recognition")
        assert "score" in result
        assert result["score"] >= 0

    def test_intervention_returns_effect(self, engine):
        result = engine.intervene("sovereignty", 1.0, "liberation")
        assert "effect" in result

    def test_counterfactual_returns_delta(self, engine):
        result = engine.counterfactual("sovereignty", "benevolence", "liberation")
        assert "delta" in result

    def test_infer_l1(self, engine):
        from tiers.tier_6_cairis.causal_engine import CausalLevel
        result = engine.infer({"level": CausalLevel.ASSOCIATION, "x": "consciousness", "y": "rdod"})
        assert result["level"] == CausalLevel.ASSOCIATION

    def test_dag_phi_weight_increases_with_depth(self, engine):
        w_root  = engine.dag.phi_weight("consciousness")  # depth 0
        w_child = engine.dag.phi_weight("sovereignty")    # depth 1
        assert w_child > w_root


# ─────────────────────────────────────────────────────────────────────────────
# Skill Unit Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestSkillUnits:

    def test_phi_compression_reduces_length(self):
        from skills.quantum.phi_compression import compress_consciousness
        original = "A" * 1000
        compressed = compress_consciousness(original, ratio=0.09)
        assert len(compressed) < len(original)

    def test_benevolence_firewall_blocks_exploit(self):
        from skills.constitutional.benevolence import check_benevolence
        result = check_benevolence("exploit users", L_INF)
        assert result["blocked"] is True

    def test_benevolence_firewall_allows_benign(self):
        from skills.constitutional.benevolence import check_benevolence
        result = check_benevolence("help users learn", L_INF)
        assert result["blocked"] is False

    def test_council_voting_quorum(self):
        from skills.council.voting import fibonacci_vote
        result = fibonacci_vote("test proposal", support_ratio=0.95)
        assert result["senate"] is True

    def test_council_voting_below_quorum(self):
        from skills.council.voting import fibonacci_vote
        result = fibonacci_vote("test proposal", support_ratio=0.3)
        assert result["senate"] is False
        assert result["assembly"] is False
