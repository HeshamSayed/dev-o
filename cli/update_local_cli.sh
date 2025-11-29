#!/bin/bash
# Script to update local devo CLI with streaming support

echo "==================================================="
echo "  DEVO CLI - Streaming Update Script"
echo "==================================================="
echo ""
echo "This will update your local devo CLI with real-time streaming support."
echo ""
echo "Instructions:"
echo "1. Copy this file to your local machine"
echo "2. Run: bash update_local_cli.sh"
echo ""
echo "Or download the updated chat_panel.py manually:"
echo "  scp root@YOUR_SERVER:/opt/application/devo_code/cli/ui/chat_panel.py ."
echo ""
echo "Then copy it to:"
echo "  ~/.devo/venv/lib/python*/site-packages/devo/ui/chat_panel.py"
echo ""
echo "==================================================="
echo ""

# Check if running on local machine
if [ -f "/home/heshamsayed/.devo/venv/bin/devo" ]; then
    echo "✓ Found local devo installation"

    # Find the site-packages directory
    SITE_PACKAGES=$(find ~/.devo/venv/lib -type d -name "site-packages" | head -1)

    if [ -z "$SITE_PACKAGES" ]; then
        echo "✗ Could not find site-packages directory"
        exit 1
    fi

    echo "  Site-packages: $SITE_PACKAGES"

    # Check if devo package exists
    if [ ! -d "$SITE_PACKAGES/devo" ]; then
        echo "✗ Devo package not found in site-packages"
        exit 1
    fi

    echo "  Devo package: $SITE_PACKAGES/devo"

    # Backup existing file
    if [ -f "$SITE_PACKAGES/devo/ui/chat_panel.py" ]; then
        cp "$SITE_PACKAGES/devo/ui/chat_panel.py" "$SITE_PACKAGES/devo/ui/chat_panel.py.backup"
        echo "✓ Backed up existing chat_panel.py"
    fi

    # Copy updated file
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    if [ -f "$SCRIPT_DIR/ui/chat_panel.py" ]; then
        cp "$SCRIPT_DIR/ui/chat_panel.py" "$SITE_PACKAGES/devo/ui/chat_panel.py"
        echo "✓ Updated chat_panel.py"

        # Clear Python cache
        find "$SITE_PACKAGES/devo" -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
        find "$SITE_PACKAGES/devo" -name "*.pyc" -delete 2>/dev/null
        echo "✓ Cleared Python cache"

        echo ""
        echo "==================================================="
        echo "  ✓ Update Complete!"
        echo "==================================================="
        echo ""
        echo "Now try: devo"
        echo "You should see real-time streaming!"

    else
        echo "✗ Could not find chat_panel.py in script directory"
        echo "  Make sure this script is in the CLI directory"
        exit 1
    fi
else
    echo "This appears to be the server. Run this script on your local machine."
    exit 1
fi
