# Raspberry Pi Art Display

A wall-mounted digital art frame powered by Raspberry Pi with smart capabilities including presence detection, time-of-day awareness, and utility features.

## Overview

The Raspberry Pi Art Display is a full-screen web application that transforms your Raspberry Pi into an aesthetic digital art frame. It automatically cycles through artwork from your local collection and includes intelligent features to enhance your experience while conserving energy.

## Features

- **Artwork Slideshow**: Automatically cycles through local image collection (JPG, PNG)
- **Presence Detection**: Detects when you're home via WiFi network scanning and adjusts display accordingly
- **Time-of-Day Awareness**: Adapts content or behavior based on time periods (day/night)
- **TODO Dashboard**: Displays a personal TODO list as an overlay or dedicated view
- **Remote Management**: Full SSH access for configuration and control
- **Future**: Support for algorithmic art generation via Python scripts

## Architecture

### Backend (Python)
- Flask web server providing REST API
- Background service for network presence detection
- File system handlers for images and TODO list
- Time-based content adaptation

### Frontend (Web)
- HTML/CSS/JavaScript single-page application
- Full-screen image viewer with smooth transitions
- TODO list overlay with distance-legible formatting
- State management polling backend for updates

### Deployment
- Runs in Chromium kiosk mode (full-screen, no UI)
- Systemd service for auto-start on boot
- Configuration via JSON files

## Requirements

### Hardware
- Raspberry Pi 2 (or newer)
- HDMI-compatible display
- WiFi connection

### Software
- Raspberry Pi OS
- Python 3.10+
- Chromium browser

## Quick Start

### Automated Installation (Recommended)

```bash
cd /home/pi
git clone <repository-url> art-display
cd art-display
./deployment/setup.sh
```

This script will:
- Install system dependencies
- Set up Python environment
- Install systemd service
- Configure autostart

### Manual Installation

See [deployment/DEPLOYMENT.md](deployment/DEPLOYMENT.md) for detailed instructions.

### Development Mode

```bash
# Install dependencies
uv venv
uv pip install -r requirements.txt

# Start backend
uv run python backend/app.py

# Open frontend
open http://localhost:5000
```

## Project Structure

```
.
├── backend/          # Python Flask server
├── frontend/         # HTML/CSS/JS web app
├── config/           # Configuration files
├── docs/             # Documentation
├── cover art/        # Image collection directory
└── requirements.txt  # Python dependencies
```

## Documentation

- **[User Guide](docs/USER_GUIDE.md)** - Daily usage and content management
- **[Configuration Guide](docs/CONFIGURATION.md)** - All configuration options explained
- **[Deployment Guide](deployment/DEPLOYMENT.md)** - Complete setup instructions
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions

## Configuration

Settings are managed via `config/config.json`:
- Image slideshow duration
- Target device IP for presence detection
- File paths and directories
- Time period definitions (day/night)
- Scan intervals

Example:
```json
{
  "image_duration": 30,
  "device_ip": "192.168.1.100",
  "paths": {
    "images": "cover art",
    "todos": "todos.txt"
  }
}
```

See [Configuration Guide](docs/CONFIGURATION.md) for all options.

## Testing

Run the integration test suite:

```bash
# Start backend
uv run python backend/app.py &

# Run tests
uv run python tests/integration_test.py
```

## API Endpoints

The backend provides these REST API endpoints:

- `GET /health` - Health check
- `GET /api/config` - Get configuration
- `GET /api/images` - List available images
- `GET /api/images/<filename>` - Serve image file
- `GET /api/todos` - Get TODO list
- `GET /api/time-period` - Get current time period (day/night)
- `GET /api/presence` - Get device presence status

## Development Status

✅ **Complete!** All core features implemented and tested.

See `tasks.md` for detailed implementation progress.

## License

Personal project - All rights reserved
