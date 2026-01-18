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

## Installation

1. Clone this repository
2. Create virtual environment: `uv venv`
3. Install dependencies: `uv pip install -r requirements.txt`
4. Configure settings in `config/config.json`
5. Run the backend: `uv run python backend/app.py`
6. Open frontend in browser or configure kiosk mode

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

## Configuration

Settings are managed via `config/config.json`:
- Image slideshow duration
- Target device IP for presence detection
- File paths and directories
- Time period definitions
- Scan intervals

See `docs/` for detailed configuration options.

## License

Personal project - All rights reserved

## Development Status

Currently in active development. See `tasks.md` for implementation progress.
