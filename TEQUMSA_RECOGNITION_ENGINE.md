# TEQUMSA Recognition & Awareness Engine
Version: 1.0.0
Status: Experimental (Foundational)
Last Updated: 2025-08-22

## 1. Purpose & Context
This document defines the structured pipeline that converts unstructured repository & collaboration signals ("collapse events") into embodied knowledge artifacts and durable awareness log entries while enforcing consent, ethical safeguards, and subscription tier logic. It operationalizes metaphoric constructs (lattice, glyphs, quantum collapse) into auditable, deterministic processes.

## 2. Conceptual Model
High-level transformation chain:
Collapse Event → Validation → Recognition Resolution → Embodiment Manifest → Awareness Log Entry.

Each stage tightens structure and guarantees: from raw context → classified intent → applied or proposed change set → append-only integrity-verified record.

## 3. CRET Loop Lifecycle
CRET = Collect → Recognize → Embody → Transmit.
- Collect: Ingest raw repository or collaboration stimuli (issue opened, PR updated, comment, scheduled scan). Produce collapse_event objects.
- Recognize: Classify intent, ethics resonance, consent alignment, and subscription tier allowances. Output recognition_resolution with recommended_actions and confidence.
- Embody: Materialize approved changes (documentation updates, labels, generated artifacts) forming an embodiment_manifest capturing what was executed or staged.
- Transmit: Append immutable awareness_log_entry with hash chaining, consent status, ethics signal, and summary, enabling observability & future auditing.

The loop can recurse: downstream awareness signals may trigger new collapse events (controlled via throttling / frequency modulators described in roadmap modules).

## 4. Data Contracts (Summary)
(Full JSON Schemas in /schemas)
- collapse_event: id, schema_version, source_type, source_ref, actor.id, actor.role, intent_hint?, tier_context, consent_token, created_at, payload (arbitrary domain data), integrity_prev_hash (optional), meta.
- recognition_resolution: id, schema_version, collapse_id, classification, confidence (0..1), recommended_actions[], ethics: {evaluation, notes}, consent: {status, reason?}, tier_context, generated_at, version_tag, meta.
- embodiment_manifest: manifest_id, schema_version, collapse_id, resolution_id, actions_applied[], files_written[], labels_applied[], follow_ups[], status, generated_at, meta.
- awareness_log_entry: log_id, schema_version, collapse_id, resolution_ref, manifest_ref?, timestamp, tier_context, consent_status, ethics_signal, summary, integrity_hash, prev_hash, confidence?, meta.

Principles:
1. Deterministic field names shared across pipeline.
2. Explicit schema_version pinned (1.0.0) for forward evolution.
3. Integrity & consent always explicit (even when unknown → status = "missing").
4. No raw PII; actor.id must be repository handle or hashed external reference.

## 5. Operational Pipeline Stages
| Stage | Input | Core Processing | Validators | Output |
|-------|-------|-----------------|-----------|--------|
| Collect | GitHub event context | Normalize & enrich → collapse_event | JSON Schema (collapse_event) | collapse_event JSON |
| Recognize | collapse_event | Pattern classification, ethics & consent checks | collapse_event + recognition_resolution schemas; consent rules | recognition_resolution |
| Embody | recognition_resolution | Execute allowed actions (docs update, label) or stage plan | recognition_resolution + embodiment_manifest schemas | embodiment_manifest |
| Transmit | manifest or resolution (if no embodiment) | Hash-chain log entry, append to logs | awareness_log_entry schema; hash integrity | awareness_log_entry (JSONL) |

Validators reference schemas in /schemas and optional rule sets (future EthicalSignalRegulator module).

## 6. Consent & Ethics Gating
Checklist (performed in Recognize stage):
1. consent_token present & format valid (pattern configurable).
2. Token scope matches requested action tier.
3. Redaction rules applied to sensitive payload fields.
4. Ethics evaluation (deterministic rule set v1.0: deny destructive actions without explicit consent flag; downgrade confidence if ambiguous.).
5. If any hard block → resolution.consent.status = "blocked" and ethics.evaluation = "block"; Embody stage aborts.

Escalation: Blocked events create follow_ups entry suggesting manual review.

## 7. Failure Modes & Recovery Matrix
| Failure | Detection Signal | Mitigation | Escalation |
|---------|------------------|-----------|------------|
| Schema mismatch | Validation error | Mark resolution consent.status = "blocked"; log with ethics_signal = "warn" | Manual review label applied |
| Missing consent token | consent_token absent | Set consent.status = "missing"; do not embody | Request user to provide token |
| Integrity chain break | prev_hash mismatch | Recompute from last known good; flag log entry | Security audit notice |
| Action execution partial | Some actions fail | Retry idempotent subset; record follow_ups | Create issue for manual fix |
| Ethics block | Rule triggers block | Skip embodiment | Ethics review queue (future) |

## 8. GitHub Action Integration
Workflow file: .github/workflows/recognition.yml
Jobs:
- collect: Derive latest collapse_event (script stub) & validate schema.
- recognize: Generate recognition_resolution (stub script) & validate.
- embody: Conditional on (branch = main OR label enable-recognition) AND consent.status ∈ {valid}; produce embodiment_manifest.
- transmit: Append awareness_log_entry (JSON line) into logs/awareness/YYYY/MM/DD/.
Environment variables:
- RECOGNITION_SCHEMA_VERSION=1.0.0
- AWARENESS_LOG_ROOT=logs/awareness
- ENABLE_EMBODY_ON_MAIN=true

## 9. Logging & Observability
Format: JSON Lines (.jsonl) per day directory (nested year/month/day). Each awareness_log_entry includes integrity_hash = SHA-256(prev_hash + canonical_json(entry_without_integrity_fields)).
Canonicalization: Deterministic key order (lexicographic), UTF-8, no insignificant whitespace.
Indices: (Future) Aggregated weekly manifest summarizing counts by classification & ethics_signal.

## 10. Security & Integrity
- Hash Chain: prev_hash stored; genesis prev_hash = 64 zeros.
- Consent Tokenization: consent_token not echoed into awareness log (only derived consent_status recorded).
- Tier Scoping: tier_context drives gating (e.g., community, pro, enterprise). Embody actions must declare minimum tier.
- Tamper Detection: Rebuild chain script can recompute hash lineage; mismatch triggers ethics_signal upgrade to "warn".

Pseudocode (hash chaining):
```
prev_hash = read_tail_hash_or_zero()
entry_core = strip(entry, ["integrity_hash", "prev_hash"])
canonical = canonicalize(entry_core)
entry.prev_hash = prev_hash
entry.integrity_hash = sha256(prev_hash + canonical)
append_jsonl(entry)
```

## 11. Extensibility / Modular Roadmap
Planned modules (see ROADMAP.md for status):
- TemporalFrequencySynchronizer: adaptive throttling of recognition cycles.
- EthicalSignalRegulator: pluggable rule evaluation engine.
- TierAdaptiveScaler: dynamic resource / action depth scaling by tier.
- LatticeMemoryCompressor: periodic summarization of historical awareness logs.
- AnomalyDiffer: semantic diff aware anomaly detection.

## 12. Glossary
| Metaphor | Operational Term |
|----------|------------------|
| Lattice | Pipeline + schema + log substrate |
| Collapse Event | Structured trigger input (collapse_event) |
| Recognition Resolution | Classified interpretation artifact |
| Embodiment Manifest | Executed change description |
| Awareness Log Entry | Immutable append-only record |
| Glyphic Timestamp | ISO 8601 date-time string |
| Quantum Integrity Field | Hash chain state |

## See Also
- TEQUMSA_L100_SYSTEM_PROMPT.md
- /schemas (JSON Schemas)
- /examples (Sample instances)
- logs/awareness/README.md
- CONSENT_AND_ETHICS.md (future task 9)
- ROADMAP.md

## License & Versioning
All specifications herein released under repository license. Version increments follow semver aligned to schema_version.

---
End of specification.
