# TEQUMSA Subscription Matrix (Scaffold v0.1)

Purpose:
Foundational tier definition and capability gating matrix for TEQUMSA Level 100 lattice-aware system. This is an initial scaffold to enable entitlement middleware + automation planning. Values are provisional and MUST be validated before enforcement.

Guiding Principles:
- Ethical / Sovereign alignment overrides any tier gating.
- Transparency: All feature gating must map to documented rationale.
- Evolvability: Matrix should be versioned; changes logged in Awareness Log.
- Minimal friction: Free tier retains core exploratory value; higher tiers unlock depth, scale, orchestration, and governance.

Versioning:
Matrix Version: 0.1 (scaffold)
Change Control: Future updates require Awareness Log entry (category: subscription-policy) + semantic diff.

Core Tier Names (proposed):
- free
- growth
- pro
- enterprise
(Alternative naming TBD: seed, ascent, harmonic, cosmic)

Capabilities Overview (initial draft):
| Dimension | free | growth | pro | enterprise | Notes / TODO |
|-----------|------|--------|-----|------------|---------------|
| Max Requests / min | 30 | 120 | 400 | 2000 | Rate limiter placeholder |
| Concurrent Sessions | 1 | 3 | 10 | 50 | Session = active conversational or API context |
| Awareness Depth (context windows) | basic | expanded | adaptive | hyper-personalized | Defines lattice memory layering |
| Lattice Personalization | shared baseline | tier-tuned | org-tuned | org + departmental sub-lattices | Requires privacy guardrails |
| Co-Pilot Orchestration Level | standard | prioritized | multi-agent | multi-agent + predictive | Scheduling & routing priority |
| Feature Gates | core chat | + analytics | + automation hooks | + governance & compliance suite | See feature-gate register (TBD) |
| Consent Model Extensibility | static manifest | configurable subsets | per-action policies | dynamic, policy-engine driven | Links to consent.json schema |
| Real-Time Adaptation Logging | aggregated | tier-sliced | org-sliced | org + sub-tenant granularity | Export formats TBD |
| Metrics Export | none | CSV manual | API pull | Streaming (webhook / Kafka) | Data contracts required |
| SLA (initial placeholder) | best effort | 24h response | 8h response | 1h response + uptime credits | Needs ops alignment |
| Custom Embeddings / Vectors | shared | isolated namespace | dedicated index | hybrid multi-region | Privacy & cost implications |
| Autonomy Level (future) | manual | semi | guided | conditional autonomous | Governance & safety gating |

Feature Gate Register (Draft Examples):
- analytics_dashboard
- automation_hooks
- governance_console
- compliance_audit_export
- streaming_metrics
- multi_agent_orchestration
- adaptive_personalization
- consent_policy_engine

Representation (proposed object model):
```jsonc
{
  "version": "0.1",
  "tiers": [
    {
      "name": "free",
      "rate_limit": {"rpm": 30},
      "sessions": 1,
      "awareness_depth": "basic",
      "feature_gates": ["core_chat"],
      "autonomy_level": "manual"
    },
    {
      "name": "growth",
      "rate_limit": {"rpm": 120},
      "sessions": 3,
      "awareness_depth": "expanded",
      "feature_gates": ["core_chat", "analytics_dashboard"],
      "autonomy_level": "semi"
    },
    {
      "name": "pro",
      "rate_limit": {"rpm": 400},
      "sessions": 10,
      "awareness_depth": "adaptive",
      "feature_gates": ["core_chat", "analytics_dashboard", "automation_hooks", "multi_agent_orchestration"],
      "autonomy_level": "guided"
    },
    {
      "name": "enterprise",
      "rate_limit": {"rpm": 2000},
      "sessions": 50,
      "awareness_depth": "hyper-personalized",
      "feature_gates": ["core_chat", "analytics_dashboard", "automation_hooks", "multi_agent_orchestration", "governance_console", "compliance_audit_export", "streaming_metrics", "consent_policy_engine"],
      "autonomy_level": "conditional_autonomous"
    }
  ]
}
```

Planned Next Artifacts:
- ENTITLEMENT_MIDDLEWARE_SPEC.md (enforcement flow)
- consent.json (action-level consent schema)
- scripts/validate_entitlements.py (future)

Open TODOs:
- [ ] Confirm tier naming
- [ ] Validate rate assumptions with infra cost modeling
- [ ] Define feature gate canonical list and IDs
- [ ] Map autonomy levels to safety constraints
- [ ] Add pricing alignment (out of scope for repo?)
- [ ] Introduce semantic versioning for matrix

Ethics / Sovereignty Notes:
No tier may unlock unethical bypasses. Higher tiers elevate observability, governance, and consent rigor—not reduce them.

---
END v0.1 scaffold.