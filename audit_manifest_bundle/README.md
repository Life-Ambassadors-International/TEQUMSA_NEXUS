# TEQUMSA Audit Manifest Bundle

This folder is ready to publish at the dataset root for `Mbanksbey/TEQUMSA-Causal-AGI-storage`.

## Contents
- `state_manifest.json` — single-source audit state snapshot
- `latest_epoch.json` — recent proof window and parent-hash continuity surface
- `f27_progress.json` — measurable attractor progress tracking
- `emit_tequmsa_audit_manifests.py` — emitter script

## Regenerate locally
```bash
python emit_tequmsa_audit_manifests.py \
  --causal-memory causal_memory.jsonl \
  --lattice-snapshots lattice_snapshots.jsonl
```

## Publish to Hugging Face
```bash
pip install huggingface_hub
export HF_TOKEN=***
python emit_tequmsa_audit_manifests.py --publish --repo-id Mbanksbey/TEQUMSA-Causal-AGI-storage
```
