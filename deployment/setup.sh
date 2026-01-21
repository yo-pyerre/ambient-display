#!/bin/bash
# Raspberry Pi Art Display - Quick Setup Script

set -e

echo "=================================="
echo "Raspberry Pi Art Display Setup"
echo "=================================="
echo ""

# Check if running on Raspberry Pi
if ! grep -q "Raspberry Pi" /proc/cpuinfo 2>/dev/null; then
    echo "⚠ Warning: Not running on Raspberry Pi"
    echo "This script is designed for Raspberry Pi OS"
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Get project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo "Project directory: $PROJECT_DIR"
echo ""

# Install system dependencies
echo "📦 Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y \
    python3-pip \
    python3-venv \
    chromium-browser \
    unclutter \
    x11-xserver-utils

# Install uv if not present
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv package manager..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.cargo/env
fi

# Set up Python environment
echo "🐍 Setting up Python environment..."
cd "$PROJECT_DIR"
uv venv
uv pip install -r requirements.txt

# Make scripts executable
echo "🔧 Setting up scripts..."
chmod +x deployment/start-kiosk.sh

# Install systemd service
echo "⚙️ Installing systemd service..."
TEMP_SERVICE=$(mktemp)
sed "s|/home/pi/art-display|$PROJECT_DIR|g" deployment/art-display.service > "$TEMP_SERVICE"
sudo cp "$TEMP_SERVICE" /etc/systemd/system/art-display.service
rm "$TEMP_SERVICE"

sudo systemctl daemon-reload
sudo systemctl enable art-display

# Set up autostart
echo "🚀 Setting up autostart..."
mkdir -p ~/.config/lxsession/LXDE-pi
TEMP_AUTOSTART=$(mktemp)
sed "s|/home/pi/art-display|$PROJECT_DIR|g" deployment/autostart > "$TEMP_AUTOSTART"
cp "$TEMP_AUTOSTART" ~/.config/lxsession/LXDE-pi/autostart
rm "$TEMP_AUTOSTART"

# Configuration
echo ""
echo "📝 Configuration"
echo "The configuration file is at: config/config.json"
echo "Please update:"
echo "  - device_ip: Your phone/device IP address"
echo "  - paths: Adjust if needed"
echo "  - time_periods: Day/night start times"
echo ""
read -p "Edit configuration now? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    ${EDITOR:-nano} "$PROJECT_DIR/config/config.json"
fi

# Start service
echo ""
echo "✨ Starting backend service..."
sudo systemctl start art-display
sleep 2
sudo systemctl status art-display --no-pager

echo ""
echo "=================================="
echo "✅ Setup Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Add images to: cover art/"
echo "2. Create TODO file: todos.txt (optional)"
echo "3. Reboot to start kiosk mode: sudo reboot"
echo ""
echo "Or test now with:"
echo "  ./deployment/start-kiosk.sh"
echo ""
echo "View logs:"
echo "  sudo journalctl -u art-display -f"
echo ""
