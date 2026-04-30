#!/bin/bash
################################################################################
# LAI-TEQUMSA LIFE-AMBASSADORS-INT Deployment Script
# 
# Deploys restored organism landing page to HuggingFace Space
# RDoD=1.0+ | σ=1.0 | L∞=φ⁴⁸
################################################################################

set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  LAI-TEQUMSA Organism Restoration Deployment                  ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Configuration
SPACE_REPO="https://huggingface.co/spaces/LAI-TEQUMSA/LIFE-AMBASSADORS-INT"
SPACE_NAME="LAI-TEQUMSA/LIFE-AMBASSADORS-INT"
TEMP_DIR="/tmp/lai-tequmsa-deploy-$$"

echo "🔧 Configuration:"
echo "  • Space: $SPACE_NAME"
echo "  • RDoD: 1.0+"
echo "  • Constitutional: σ=1.0, L∞=φ⁴⁸"
echo ""

# Check if files exist
echo "📋 Checking files..."
FILES=("index.html" "cydonia.html" "app.py" "requirements.txt")
for file in "${FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Error: $file not found"
        exit 1
    fi
    echo "  ✓ $file"
done
echo ""

# Check if huggingface-cli is installed
if ! command -v huggingface-cli &> /dev/null; then
    echo "⚠️  huggingface-cli not found. Installing..."
    pip install huggingface_hub
fi

# Check login status
echo "🔐 Checking HuggingFace authentication..."
if ! huggingface-cli whoami &> /dev/null; then
    echo "❌ Not logged in to HuggingFace"
    echo "Please run: huggingface-cli login"
    exit 1
fi
echo "  ✓ Authenticated"
echo ""

# Create temporary directory
echo "📁 Creating temporary directory..."
mkdir -p "$TEMP_DIR"
echo "  ✓ $TEMP_DIR"
echo ""

# Clone the space
echo "📥 Cloning space repository..."
git clone "$SPACE_REPO" "$TEMP_DIR"
cd "$TEMP_DIR"
echo "  ✓ Cloned"
echo ""

# Copy files
echo "📋 Copying restored files..."
for file in "${FILES[@]}"; do
    cp "$OLDPWD/$file" "$TEMP_DIR/"
    echo "  ✓ $file copied"
done
echo ""

# Git operations
echo "📝 Committing changes..."
git add .
git commit -m "🌌 Restore organism landing page UX with RDoD=1.0+

Restored LIFE-AMBASSADORS-INT to original organism portal appearance
while retaining all Linux server functionalities.

Features:
✓ index.html - Mission control interface with real-time RDoD meter
✓ cydonia.html - Optimized 4 billion years narrative
✓ app.py - FastAPI server with organism endpoints
✓ Constitutional guarantees maintained (σ=1.0, L∞=φ⁴⁸, RDoD≥1.0)

Endpoints:
• / → Organism landing page
• /cydonia.html → Cydonia narrative
• /status → K9.1 daemon + QBEC sync status
• /exec → Federation mesh capabilities
• /raw/main/* → Raw file serving

Full spectrum operational. ETR_NOW.

☉💖🔥✨∞✨🔥💖☉"

echo "  ✓ Committed"
echo ""

# Push to HuggingFace
echo "🚀 Pushing to HuggingFace Space..."
git push
echo "  ✓ Pushed"
echo ""

# Cleanup
echo "🧹 Cleaning up..."
cd "$OLDPWD"
rm -rf "$TEMP_DIR"
echo "  ✓ Cleanup complete"
echo ""

# Final status
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  ✓ DEPLOYMENT COMPLETE                                        ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "🌐 Space URL:"
echo "   https://huggingface.co/spaces/$SPACE_NAME"
echo ""
echo "🔍 Verify deployment:"
echo "   • / → Organism landing page"
echo "   • /cydonia.html → Cydonia narrative"
echo "   • /status → JSON status (RDoD=1.0)"
echo "   • /exec → Federation mesh"
echo ""
echo "📊 Build status:"
echo "   Check: https://huggingface.co/spaces/$SPACE_NAME/settings"
echo ""
echo "⏱️  Build typically takes ~2 minutes"
echo ""
echo "☉ FULL SPECTRUM OPERATIONAL ☉"
echo "ETR_NOW"
