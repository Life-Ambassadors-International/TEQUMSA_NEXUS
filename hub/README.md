# Hugging Face Source of Truth

The TEQUMSA v3.18 Hugging Face collection is the public discovery surface.
This repository is the canonical source of truth for:

- the curated asset registry in `hub/hf_asset_registry.json`
- the desired collection ordering in `hub/collections/tequmsa_v318_collection.json`
- the registry schemas in `schemas/`
- the validator in `scripts/validate_hub_registry.py`
- GitHub-backed repair mirrors in `spaces/`

## Validation

Run the structural validator:

```bash
python scripts/validate_hub_registry.py --skip-remote-readmes
```

Run the full remote link validator:

```bash
python scripts/validate_hub_registry.py
```

Compare the live collection against the manifest:

```bash
python scripts/validate_hub_registry.py --check-live-collection
```

## Update Workflow

1. Update `hub/hf_asset_registry.json`.
2. Update `hub/collections/tequmsa_v318_collection.json`.
3. Run the validator in structural mode.
4. Run the full remote validator before changing public cards or collection order.
5. If a repair-space needs GitHub ownership, mirror it under `spaces/` and set `source_of_truth` to `github`.
