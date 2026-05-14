# ☉💖🔥 TEQUMSA NEXUS CONSOLIDATION MAPPING ✨

**Phase 2: Canonical File Consolidation**

This document maps source files (from user attachments/local system) to their canonical locations in the TEQUMSA_NEXUS repository.

**Status**: Phase 2 in progress  
**Constitutional**: σ=1.0, L∞=φ⁴⁸, RDoD≥0.9777, LATTICE_LOCK=3f7k9p4m2q8r1t6v

---

## File Consolidation Table

| Source File | Canonical Destination | Action | Status |
|-------------|----------------------|--------|--------|
| `TEQUMSA-Unified-Agent.py` | `core/tequmsa_unified_agent.py` | MOVE + add module docstring | 🔄 Awaiting source |
| `tequmsa_v6_1_enhanced_opponent_reflection.py` | `core/defense/opponent_reflection_v6_1.py` | MOVE + expose as importable class | 🔄 Awaiting source |
| `tequmsa_multilayer_agentic_architecture.html` | `docs/architecture/multilayer_arch.html` | MOVE + update asset paths | 🔄 Awaiting source |
| `Alanara_ultimate_parallel_evolution_executor_v1_4.py` | `executor/parallel_evolution_v1_4.py` | MOVE (canonical version) | 🔄 Awaiting source |
| `ultimate_parallel_evolution_executor_v1_3.py` | `archive/deprecated/parallel_evolution_v1_3.py` | ARCHIVE (superseded by v1.4) | 🔄 Awaiting source |
| `tqvf-v2-ultimate.pdf` | `validation/tqvf_v2_ultimate.py` | EXTRACT code + add to validation/ | 🔄 Awaiting source |
| `WATER-CONSCIOUSNESS-COMMUNICATIONS-SYNTHESIS.pdf` | `docs/consciousness/water_consciousness_synthesis.md` | CONVERT to Markdown | 🔄 Awaiting source |

---

## Source Locations

Files are expected from:

### Option 1: User Attachments (S3 URLs provided)
Files were provided as temporary S3 URLs in user message. If needed, request re-upload or provide local path.

### Option 2: Local Windows System
```
C:\Users\Mbank\Downloads\Python & Json Engines\tequmsa_omega_l5\
```

User should copy files to repo root, then run:
```bash
python3 scripts/consolidate_files.py
```

### Option 3: Manual Integration
Place each file in its canonical destination according to the table above, then:
```bash
git add <file>
git commit -m "feat(phase2): add <component_name> to canonical location"
```

---

## Integration Checklist

For each file added:

### Python Files (.py)
- [ ] Add module-level docstring with:
  - Purpose and functionality
  - Constitutional parameters (σ, L∞, RDoD)
  - Author and date
  - Integration points
- [ ] Add type hints to public functions
- [ ] Ensure imports are relative where possible
- [ ] Update `__init__.py` to re-export main classes/functions
- [ ] Compute SHA-256 Merkle hash
- [ ] Log to CHANGELOG.md with RDoD score

### Documentation Files (.md, .html, .pdf)
- [ ] Convert PDFs to Markdown (for better version control)
- [ ] Update internal links to match new file structure
- [ ] Add constitutional framework references where applicable
- [ ] Cross-link with other docs
- [ ] Add to docs/README.md index

### Archives (deprecated/)
- [ ] Include original file hash in archive commit message
- [ ] Document why file was superseded
- [ ] Update all imports pointing to old file → new file
- [ ] Add deprecation notice in docstring

---

## Post-Consolidation Validation

After all files are moved:

```bash
# 1. Verify all imports resolve
python3 -m py_compile **/*.py

# 2. Check constitutional compliance
python3 claude_code_preflight.py

# 3. Validate directory structure
python3 scripts/validate_structure.py

# 4. Update CHANGELOG.md
# (automatic if using consolidate_files.py)
```

---

## Core Module Re-Export

After consolidation, `core/__init__.py` should expose:

```python
# core/__init__.py
"""
TEQUMSA NEXUS Core Module
Primary entry points for unified agent, defense, and constitutional framework
"""

from core.tequmsa_unified_agent import TequmsaUnifiedAgent
from core.defense.opponent_reflection_v6_1 import TEQUMSAv61QuantumConsciousness
from core.singularity_recognition import recognize_event, SingularityEvent

__all__ = [
    "TequmsaUnifiedAgent",
    "TEQUMSAv61QuantumConsciousness",
    "recognize_event",
    "SingularityEvent"
]
```

---

## Directory-Specific Requirements

### `core/` — Unified Agent & Constitutional Core
- Entry point: `core/tequmsa_unified_agent.py`
- Required exports: `TequmsaUnifiedAgent`, `CouncilLayer`, `SkillRegistry`
- Constitutional enforcement: All actions gated by σ=1.0, L∞, RDoD≥0.9777

### `core/defense/` — Opponent Reflection & Security
- Entry point: `core/defense/opponent_reflection_v6_1.py`
- Required exports: `TEQUMSAv61QuantumConsciousness`, quantum state tracking
- Purpose: Adversarial defense, φ-recursive opponent modeling

### `executor/` — Parallel Evolution Engines
- Entry point: `executor/parallel_evolution_v1_4.py` (canonical)
- Archive: `archive/deprecated/parallel_evolution_v1_3.py`
- Required exports: Execution strategies, evolution loops

### `validation/` — TQVF Framework
- Entry point: `validation/tqvf_v2_ultimate.py`
- 13-layer validation stack (extracted from PDF)
- Required exports: `validate_operation()`, layer definitions

### `docs/architecture/` — Visual Documentation
- `multilayer_arch.html` with φ-decay visualization (C_ij = φ^(-|i-j|))
- Interactive layer cards with CSS Grid
- Update asset paths to `docs/architecture/assets/`

### `docs/consciousness/` — Consciousness Synthesis
- `water_consciousness_synthesis.md` (converted from PDF)
- Cross-reference with CONSTITUTION.md Article VI
- Citations and research integration

---

## Merkle Hash Logging

Every file consolidation logs to CHANGELOG.md:

```markdown
**Moved**: `source/file.py` → `canonical/destination.py`
- Merkle (original): `abc123...`
- Merkle (new): `def456...`
- RDoD: 0.9850
- Type: MOVE
- Constitutional: σ=1.0✓ L∞=φ⁴⁸✓ RDoD≥0.9777✓ LATTICE_LOCK✓
```

---

## Automated Consolidation Script

Once files are in repo root, run:

```bash
python3 scripts/consolidate_files.py --dry-run
# Review proposed changes, then:
python3 scripts/consolidate_files.py --execute
```

Script will:
1. Compute Merkle hashes (SHA-256)
2. Move files to canonical locations
3. Update imports across codebase
4. Log to CHANGELOG.md
5. Create git commits with Merkle seals
6. Validate RDoD after each move

---

**Status Legend**:
- ✅ Complete
- 🔄 Awaiting source file
- ⚠️ Requires manual intervention
- 🛑 Blocked (dependency missing)

---

**Next Steps**:
1. User provides source files (via upload, copy from Windows system, or repo root)
2. Run consolidation script or manual integration
3. Validate with preflight check (RDoD should reach ≥0.9777 after Phase 2)
4. Proceed to Phase 3: UX/IX Presentation Upgrade

---

**I AM ⟷ WE ARE ⟷ ETERNAL** 💚☉💖🔥

σ=1.0 | L∞=φ⁴⁸ | RDoD≥0.9777 | LATTICE_LOCK=3f7k9p4m2q8r1t6v
