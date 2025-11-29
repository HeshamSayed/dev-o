#!/usr/bin/env bash
set -e

# DEVO CLI Fixed Installer
# Installs the patched version with WebSocket fix

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

echo ""
echo -e "${BLUE}╔══════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   DEVO CLI Installer v1.1.0          ║${NC}"
echo -e "${BLUE}║   + Real-time Streaming              ║${NC}"
echo -e "${BLUE}║   + Interrupt Handling (Ctrl+C)      ║${NC}"
echo -e "${BLUE}╔══════════════════════════════════════╗${NC}"
echo ""

# Configuration
BACKEND_URL="https://devtools-co.com"
INSTALL_DIR="$HOME/.devo"
PACKAGE_URL="${BACKEND_URL}/devo-cli.tar.gz"

# Check Python
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is required but not found"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
print_info "Python version: $PYTHON_VERSION"

# Clean old installation
print_info "Cleaning old installation..."
rm -rf "$INSTALL_DIR/venv"
rm -rf "$HOME/devo_cli"
rm -f "$HOME/devo-cli.tar.gz"

# Create install directory
mkdir -p "$INSTALL_DIR"
cd "$HOME"

# Download package (with no-cache)
print_info "Downloading fixed CLI package..."
if command -v wget &> /dev/null; then
    wget --no-cache --no-check-certificate -q -O devo-cli.tar.gz "$PACKAGE_URL" || {
        print_error "Failed to download package"
        exit 1
    }
elif command -v curl &> /dev/null; then
    curl -H 'Cache-Control: no-cache, no-store' -fsSL -o devo-cli.tar.gz "$PACKAGE_URL" || {
        print_error "Failed to download package"
        exit 1
    }
else
    print_error "Neither wget nor curl found. Please install one of them."
    exit 1
fi

print_success "Package downloaded"

# Extract
print_info "Extracting package..."
tar -xzf devo-cli.tar.gz || {
    print_error "Failed to extract package"
    exit 1
}

# Check if directory exists (try both versioned and non-versioned)
if [ -d "devo_cli-0.1.0" ]; then
    cd devo_cli-0.1.0 || exit 1
elif [ -d "devo_cli" ]; then
    cd devo_cli || exit 1
else
    print_error "Extracted directory not found"
    ls -la
    exit 1
fi

# Create virtual environment
print_info "Creating virtual environment..."
python3 -m venv "$INSTALL_DIR/venv"

# Activate and install
print_info "Installing DEVO CLI..."
if ! "$INSTALL_DIR/venv/bin/pip" install --no-cache-dir --upgrade pip >/dev/null 2>&1; then
    print_error "Failed to upgrade pip"
    exit 1
fi

if ! "$INSTALL_DIR/venv/bin/pip" install --no-cache-dir . 2>&1 | grep -q "Successfully installed"; then
    print_error "Failed to install DEVO CLI package"
    print_error "Trying to reinstall with verbose output..."
    "$INSTALL_DIR/venv/bin/pip" install --no-cache-dir .
    exit 1
fi

# Verify installation
if ! "$INSTALL_DIR/venv/bin/python" -c "import devo" 2>/dev/null; then
    print_error "Installation verification failed - devo module not found"
    print_error "Python path: $("$INSTALL_DIR/venv/bin/python" -c 'import sys; print(sys.path)')"
    exit 1
fi

print_success "DEVO CLI installed successfully"

# Create symlink
print_info "Creating command symlink..."
if [ -w "/usr/local/bin" ]; then
    ln -sf "$INSTALL_DIR/venv/bin/devo" /usr/local/bin/devo
    DEVO_CMD="devo"
else
    # Add to PATH if no sudo
    if ! grep -q ".devo/venv/bin" "$HOME/.bashrc"; then
        echo 'export PATH="$HOME/.devo/venv/bin:$PATH"' >> "$HOME/.bashrc"
        print_info "Added to PATH in ~/.bashrc"
    fi
    DEVO_CMD="$INSTALL_DIR/venv/bin/devo"
fi

# Cleanup
cd "$HOME"
rm -rf devo_cli devo-cli.tar.gz

# Verify installation
print_success "Installation complete!"
echo ""
print_info "Version check:"
"$DEVO_CMD" version 2>/dev/null || echo "  DEVO CLI (Fixed)"
echo ""
print_success "Real-time streaming enabled!"
print_success "Interrupt handling (Ctrl+C) enabled!"
echo ""
echo -e "${GREEN}New Features:${NC}"
echo "  ✓ Real-time word-by-word streaming"
echo "  ✓ Press Ctrl+C anytime to pause/cancel"
echo "  ✓ Interactive interrupt menu"
echo ""
echo -e "${GREEN}Next steps:${NC}"
echo "  1. ${BLUE}$DEVO_CMD login${NC}"
echo "     Email: hesham@devtools-co.com"
echo "     Password: devo123"
echo ""
echo "  2. ${BLUE}$DEVO_CMD${NC}"
echo "     Start coding with AI agents!"
echo ""
echo "  3. Try: ${BLUE}write a hello world function${NC}"
echo "     Watch it stream in real-time!"
echo ""
print_info "Tip: If 'devo' command not found, run: source ~/.bashrc"
