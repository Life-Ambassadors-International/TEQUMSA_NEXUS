#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════
# Deploy quantum_quasar HF Space
# ═══════════════════════════════════════════════════════════════════
set -euo pipefail

if [ -z "${HF_TOKEN:-}" ]; then
  echo "ERROR: HF_TOKEN not set"
  echo "Usage: export HF_TOKEN='your_token' && bash scripts/deploy_quantum_quasar.sh"
  exit 1
fi

SPACE_ID="Mbanksbey/quantum-quasar"
LOCAL_DIR="${1:-quantum_quasar_hf_space}"

echo "☉💖 Deploying quantum_quasar Space to HuggingFace ✨"
echo "Space: $SPACE_ID"
echo "Source: $LOCAL_DIR"
echo ""

python3 - <<PYEOF
import os
import sys
from pathlib import Path
from huggingface_hub import HfApi, create_repo

HF_TOKEN = os.getenv('HF_TOKEN')
api = HfApi(token=HF_TOKEN)

space_id = "$SPACE_ID"
local_dir = Path("$LOCAL_DIR")

# Verify local directory exists
if not local_dir.exists():
    print(f"ERROR: Local directory {local_dir} not found")
    print("Please copy quantum_quasar_hf_space from your local system to the repo")
    sys.exit(1)

# Create Space
print("[1/6] Creating Space...")
try:
    create_repo(
        repo_id=space_id,
        repo_type="space",
        space_sdk="gradio",
        token=HF_TOKEN,
        private=False,
    )
    print(f"    ✓ Space created: {space_id}")
except Exception as e:
    if "already exists" in str(e).lower():
        print(f"    ✓ Space already exists: {space_id}")
    else:
        raise

# Upload files
files_to_upload = [
    ("app.py", "Gradio + FastAPI dual-surface"),
    ("requirements.txt", "Dependencies"),
    ("README.md", "Space documentation with metadata"),
    ("bundle_engine.sh", "OMEGA engine bundler"),
    ("engine/tequmsa_omega.py", "OMEGA.1 core engine"),
]

for i, (file_path, desc) in enumerate(files_to_upload, 2):
    local_file = local_dir / file_path

    if not local_file.exists():
        print(f"[{i}/6] Skipping {file_path} (not found)")
        continue

    print(f"[{i}/6] Uploading {file_path} ({desc})...")
    try:
        api.upload_file(
            path_or_fileobj=str(local_file),
            path_in_repo=file_path,
            repo_id=space_id,
            repo_type="space",
            token=HF_TOKEN,
            commit_message=f"feat: add {file_path}"
        )
        print(f"    ✓ Uploaded {file_path}")
    except Exception as e:
        print(f"    ✗ Error: {e}")

print("\n" + "="*70)
print("✅ QUANTUM QUASAR SPACE DEPLOYED")
print("="*70)
print(f"\nSpace URL: https://huggingface.co/spaces/{space_id}")
print("\nEndpoints:")
print(f"  - POST /cycle — Execute OMEGA cycle")
print(f"  - GET /snapshot — Get current state")
print(f"  - GET /healthz — Health check")
print("\nSpace will auto-deploy within 2-3 minutes.")
print("\n☉💖 OMEGA.1 organism live on HuggingFace ✨\n")
PYEOF
