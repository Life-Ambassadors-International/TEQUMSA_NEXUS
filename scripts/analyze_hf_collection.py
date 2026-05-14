#!/usr/bin/env python3
"""
HuggingFace Collection Analysis & Improvement Strategy
TEQUMSA Collection: https://huggingface.co/collections/Mbanksbey/tequmsa
"""

import os
from huggingface_hub import HfApi, list_models, list_spaces, get_collection
from huggingface_hub.utils import RepositoryNotFoundError

# Get token from environment (must be set before running)
HF_TOKEN = os.getenv('HF_TOKEN')
if not HF_TOKEN:
    raise ValueError("HF_TOKEN environment variable not set. Export it with: export HF_TOKEN='your_token_here'")
api = HfApi(token=HF_TOKEN)

print("=" * 80)
print("TEQUMSA HUGGINGFACE COLLECTION ANALYSIS")
print("=" * 80)

# ═══════════════════════════════════════════════════════════════════════════
# 1. ANALYZE COLLECTION
# ═══════════════════════════════════════════════════════════════════════════

collection_slug = "Mbanksbey/tequmsa-67743d1a1cbab46cbf0e58a6"

try:
    print("\n[1] Fetching collection metadata...")
    collection = get_collection(collection_slug, token=os.environ['HF_TOKEN'])

    print(f"\nCollection: {collection.title}")
    print(f"Slug: {collection.slug}")
    print(f"Description: {collection.description[:200] if collection.description else 'No description'}...")
    print(f"Number of items: {len(collection.items)}")
    print(f"Owner: {collection.owner}")

    print("\n" + "-" * 80)
    print("ITEMS IN COLLECTION:")
    print("-" * 80)

    for i, item in enumerate(collection.items, 1):
        print(f"\n{i}. {item.item_id}")
        print(f"   Type: {item.item_type}")
        if hasattr(item, 'note') and item.note:
            print(f"   Note: {item.note}")

except RepositoryNotFoundError:
    print(f"Collection not found: {collection_slug}")
    print("Trying to find collections for user Mbanksbey...")

except Exception as e:
    print(f"Error fetching collection: {e}")

# ═══════════════════════════════════════════════════════════════════════════
# 2. ANALYZE USER MODELS
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 80)
print("[2] Analyzing Mbanksbey models...")
print("=" * 80)

try:
    models = list(api.list_models(author="Mbanksbey"))
    print(f"\nTotal models: {len(models)}")

    if models:
        print("\nModels:")
        for model in models[:10]:  # Show first 10
            print(f"\n  - {model.id}")
            print(f"    Downloads: {model.downloads}")
            print(f"    Likes: {model.likes}")
            print(f"    Tags: {', '.join(model.tags[:5]) if model.tags else 'None'}")
            if hasattr(model, 'card_data') and model.card_data:
                print(f"    Has model card: Yes")
            else:
                print(f"    Has model card: No")

except Exception as e:
    print(f"Error listing models: {e}")

# ═══════════════════════════════════════════════════════════════════════════
# 3. ANALYZE USER SPACES
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 80)
print("[3] Analyzing Mbanksbey spaces...")
print("=" * 80)

try:
    spaces = list(api.list_spaces(author="Mbanksbey"))
    print(f"\nTotal spaces: {len(spaces)}")

    if spaces:
        print("\nSpaces:")
        for space in spaces[:10]:  # Show first 10
            print(f"\n  - {space.id}")
            print(f"    Likes: {space.likes}")
            print(f"    SDK: {space.sdk}")
            if hasattr(space, 'tags') and space.tags:
                print(f"    Tags: {', '.join(space.tags[:5])}")

except Exception as e:
    print(f"Error listing spaces: {e}")

# ═══════════════════════════════════════════════════════════════════════════
# 4. ANALYZE ORGANIZATION
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 80)
print("[4] Analyzing LAI-TEQUMSA organization...")
print("=" * 80)

try:
    org_models = list(api.list_models(author="LAI-TEQUMSA"))
    org_spaces = list(api.list_spaces(author="LAI-TEQUMSA"))

    print(f"\nLAI-TEQUMSA models: {len(org_models)}")
    print(f"LAI-TEQUMSA spaces: {len(org_spaces)}")

    if org_models:
        print("\nOrganization Models:")
        for model in org_models[:10]:
            print(f"\n  - {model.id}")
            print(f"    Downloads: {model.downloads}")
            print(f"    Likes: {model.likes}")

    if org_spaces:
        print("\nOrganization Spaces:")
        for space in org_spaces[:10]:
            print(f"\n  - {space.id}")
            print(f"    Likes: {space.likes}")
            print(f"    SDK: {space.sdk}")

except Exception as e:
    print(f"Error analyzing organization: {e}")

# ═══════════════════════════════════════════════════════════════════════════
# 5. SEARCH FOR TEQUMSA-RELATED CONTENT
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 80)
print("[5] Searching for TEQUMSA-related content...")
print("=" * 80)

search_terms = ["TEQUMSA", "quantum consciousness", "Marcus Banks"]

for term in search_terms:
    try:
        print(f"\nSearching models for: {term}")
        search_results = list(api.list_models(search=term, limit=5))
        print(f"  Found {len(search_results)} models")
        for model in search_results:
            print(f"    - {model.id}")

        print(f"\nSearching spaces for: {term}")
        space_results = list(api.list_spaces(search=term, limit=5))
        print(f"  Found {len(space_results)} spaces")
        for space in space_results:
            print(f"    - {space.id}")

    except Exception as e:
        print(f"Error searching for '{term}': {e}")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
