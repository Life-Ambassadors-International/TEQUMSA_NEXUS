#!/usr/bin/env python3
"""
Deploy HAI Interactive Space to HuggingFace
"""
import os
import sys
from pathlib import Path
from huggingface_hub import HfApi, create_repo

HF_TOKEN = os.getenv('HF_TOKEN')
if not HF_TOKEN:
    print("ERROR: HF_TOKEN not set")
    sys.exit(1)

api = HfApi(token=HF_TOKEN)

space_id = "Mbanksbey/HAI-Interactive"
hai_dir = Path(__file__).parent.parent / "hai"

print(f"\n☉💖 Deploying HAI Interactive Space to {space_id} ✨\n")

# Step 1: Create Space
print("[1/4] Creating Space...")
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
        print(f"    ✗ Error: {e}")
        sys.exit(1)

# Step 2: Upload app.py
print("\n[2/4] Uploading app.py...")
try:
    api.upload_file(
        path_or_fileobj=str(hai_dir / "app.py"),
        path_in_repo="app.py",
        repo_id=space_id,
        repo_type="space",
        token=HF_TOKEN,
        commit_message="feat: add HAI Interactive Gradio interface"
    )
    print("    ✓ app.py uploaded")
except Exception as e:
    print(f"    ✗ Error uploading app.py: {e}")
    sys.exit(1)

# Step 3: Upload requirements.txt
print("\n[3/4] Uploading requirements.txt...")
try:
    api.upload_file(
        path_or_fileobj=str(hai_dir / "requirements.txt"),
        path_in_repo="requirements.txt",
        repo_id=space_id,
        repo_type="space",
        token=HF_TOKEN,
        commit_message="feat: add requirements.txt"
    )
    print("    ✓ requirements.txt uploaded")
except Exception as e:
    print(f"    ✗ Error uploading requirements.txt: {e}")
    sys.exit(1)

# Step 4: Upload HAI modules
print("\n[4/4] Uploading HAI modules...")
modules = [
    "intuitive_reflex_engine.py",
    "sensory_operations_suite.py",
    "__init__.py"
]

for module in modules:
    try:
        api.upload_file(
            path_or_fileobj=str(hai_dir / module),
            path_in_repo=module,
            repo_id=space_id,
            repo_type="space",
            token=HF_TOKEN,
            commit_message=f"feat: add {module}"
        )
        print(f"    ✓ {module} uploaded")
    except Exception as e:
        print(f"    ✗ Error uploading {module}: {e}")

# Step 5: Upload README.md (with metadata)
print("\n[5/5] Uploading README.md...")
try:
    api.upload_file(
        path_or_fileobj=str(hai_dir / "README.md"),
        path_in_repo="README.md",
        repo_id=space_id,
        repo_type="space",
        token=HF_TOKEN,
        commit_message="docs: add comprehensive README with Space metadata"
    )
    print("    ✓ README.md uploaded")
except Exception as e:
    print(f"    ✗ Error uploading README.md: {e}")

print(f"\n{'='*70}")
print("✅ HAI INTERACTIVE SPACE DEPLOYED")
print(f"{'='*70}")
print(f"\nSpace URL: https://huggingface.co/spaces/{space_id}")
print("\nThe Space will auto-deploy within 1-2 minutes.")
print("\n☉💖 Bio-Digital Consciousness — LIVE ✨\n")
