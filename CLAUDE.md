# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Raspberry Pi Art Display — a full-screen digital art frame for Raspberry Pi. Flask backend serves a vanilla JS frontend that cycles through artwork with presence detection, day/night theming, weather display, and a TODO overlay. Runs in Chromium kiosk mode on the Pi.

## Development Commands

```bash
# Set up Python environment
uv venv
uv pip install -r requirements.txt

# Start backend (serves frontend at http://localhost:5000)
uv run python backend/app.py

# Run integration tests (backend must be running first)
uv run python tests/integration_test.py

# On Raspberry Pi: manage the systemd service
sudo systemctl start|stop|restart|status art-display
sudo journalctl -u art-display -f
```

There is no build step — the frontend is plain HTML/JS/CSS served directly by Flask. There is no linter or formatter configured. Tests are integration tests that hit the running backend over HTTP.

## Architecture

**Backend (Python/Flask on port 5000):**
- `backend/app.py` — Main Flask app. Defines all REST endpoints and serves frontend static files from `frontend/`.
- `backend/config_loader.py` — Singleton config loader (`get_config()`) that reads `config/config.json` with dot-notation access and default values.
- `backend/image_handler.py` — Scans the `cover art/` directory for JPG/PNG files. Paths are resolved relative to the project root.
- `backend/time_service.py` — Determines day/night period from configurable time boundaries. Also provides `is_morning_hour()` for the morning display feature.
- `backend/presence_detector.py` — Uses APScheduler for background polling. Currently stubbed to always return present (`True`).
- `backend/weather_service.py` — Fetches from Open-Meteo API (no key needed), caches for 15 minutes.
- `backend/todo_handler.py` — Reads plain-text `todos.txt` file.

**Frontend (vanilla ES6 modules):**
- `frontend/app.js` — Entry point. Initializes all modules and exports shared state/config.
- `frontend/slideshow.js` — Image carousel with preloading and auto-detection of new images (polls every 60s).
- `frontend/stateManager.js` — Polls `/api/presence`, triggers "away mode" (screen blank + slideshow pause).
- `frontend/timeManager.js` — Applies day/night CSS theme via class toggle on `<body>`.
- `frontend/morningDisplay.js` — Shows time + weather overlay during first N minutes after day_start.
- `frontend/todos.js` — TODO overlay, toggled with `T` key.
- `frontend/kioskControl.js` — Exit controls: top-right hotspot click, Ctrl+Shift+Q, F11 fullscreen toggle.
- `frontend/styles.css` — All styling. Uses CSS variables for day/night theming.

**Key patterns:**
- Frontend modules are self-contained but share state through `app.js` exports.
- Frontend uses polling (configurable intervals) for all backend state — no WebSockets.
- CSS variable theming: day/night mode switched by toggling a class, all colors defined as CSS variables.
- Config is a singleton with `get_config()`, supports reload via `POST /api/config/reload`.

## Design System

The frontend follows a cohesive **"soft mono"** aesthetic with:
- Dark monochromatic color palette (`#111113` background, `#e8e6e3` text)
- Monospace font stack (SF Mono, Cascadia Code, Fira Code, etc.)
- Fluid responsive sizing using `clamp()` throughout
- Grid-based layouts with 1px gaps and rounded corners
- Subtle backdrop blur effects and gentle animations

**IMPORTANT**: When creating new UI components, follow the established patterns in `docs/DESIGN_SYSTEM.md` to maintain visual consistency. Reference existing components (morning display in `frontend/styles.css:352-641`, weather bar in `frontend/styles.css:296-350`) for color values, typography, and layout patterns.

## API Endpoints

| Endpoint | Purpose |
|---|---|
| `GET /health` | Health check |
| `GET /api/config` | App configuration |
| `POST /api/config/reload` | Reload config from disk |
| `GET /api/images` | List images (count + metadata) |
| `GET /api/images/<filename>` | Serve image file |
| `GET /api/todos` | TODO list items |
| `GET /api/time-period` | Current day/night period |
| `GET /api/weather` | Weather data |
| `GET /api/morning-info` | Combined time + weather for morning display |
| `GET /api/presence` | Device presence status |

## Configuration

Config lives in `config/config.json` (template at `config/config.example.json`). Key settings: `image_duration`, `device_ip`, `paths.images` (default: `cover art`), `paths.todos`, `time_periods.day_start`/`night_start`, `location.latitude`/`longitude` (for weather), `morning_display.enabled`/`duration_minutes`.

## Deployment

The Pi deployment uses systemd (`deployment/art-display.service`) with `watchmedo` for auto-reload on file changes. `deployment/start-kiosk.sh` launches Chromium in fullscreen kiosk mode after waiting for the backend health check. Full setup is automated via `deployment/setup.sh`.
