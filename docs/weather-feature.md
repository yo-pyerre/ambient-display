# Weather Feature Enhancement

## Overview

Upgrade the existing barebones weather implementation into a comprehensive weather system with two display modes: an always-on bottom bar during slideshow and an enhanced morning display with full forecast data.

## Current State

- Backend fetches current temperature + WMO weather code from Open-Meteo API (15-min cache)
- Weather only shown during morning hours on a full-screen overlay (clock + temp + text description)
- No icons, no forecast, no additional conditions data, no sun/moon info
- Celsius only, no unit configuration

## Requirements

### R1: Always-On Weather Bottom Bar
- Thin persistent bar across the bottom of the screen during artwork slideshow
- Shows: current time, weather emoji, temperature, condition text
- Subtle semi-transparent design that doesn't distract from artwork
- Auto-hides when morning display is active (no duplication)
- Hides during away mode

### R2: Enhanced Morning Display
- Keep the existing full-screen overlay with large clock
- Add 5-day daily forecast row (emoji + day name + high/low temps)
- Add detail pills: feels-like temperature, humidity, wind speed, UV index
- Add sunrise/sunset times
- Add moon phase indicator
- Elegant layout using `frontend-design` skill

### R3: Expanded Weather Data (Backend)
- **Current conditions**: temperature, apparent (feels-like) temperature, humidity, wind speed, UV index, weather code
- **5-day daily forecast**: high/low temps, weather codes, sunrise/sunset times, max UV
- **Moon phase**: algorithmic calculation (synodic month formula)
- **Emoji mapping**: WMO weather codes → unicode weather emojis (☀️🌤️⛅🌥️☁️🌧️⛈️🌨️ etc.)

### R4: Temperature Units
- Default: Fahrenheit (°F)
- Configurable via `temperature_unit` in `config/config.json` (`"fahrenheit"` or `"celsius"`)
- Use Open-Meteo's `temperature_unit` API parameter for server-side conversion

### R5: Shared Weather Service (Frontend)
- Single shared module fetches from `/api/weather`
- Both bottom bar and morning display consume from the same data source
- Prevents duplicate API calls

### R6: No New Dependencies
- Vanilla JavaScript (ES6 modules), CSS, HTML only
- Unicode emojis for weather icons — no icon libraries
- No frontend frameworks or heavy packages

## Technical Design

### Backend Changes
- **`backend/weather_service.py`**: Expand API call, add emoji mapping, two-tier caching (current: 15 min, forecast: 1 hour), moon phase calculation
- **`backend/app.py`**: Update `/api/weather` and `/api/morning-info` response shapes
- **`backend/config_loader.py`**: Add `temperature_unit` default

### Frontend Changes
- **`frontend/weatherService.js`** (new): Shared weather data fetcher with subscribe/callback pattern
- **`frontend/weatherBar.js`** (new): Always-on bottom bar module
- **`frontend/morningDisplay.js`**: Enhance with forecast, details, sun/moon data
- **`frontend/index.html`**: Add bottom bar HTML, expand morning overlay
- **`frontend/styles.css`**: Bottom bar styling, enhanced morning display styling
- **`frontend/app.js`**: Initialize new modules, coordinate visibility

### Config Changes
- **`config/config.example.json`**: Add `"temperature_unit": "fahrenheit"`

## Tasks

### Phase 1: Design
- [ ] Create standalone HTML mockup files for user review (planning/mockups/)
- [ ] Iterate on chosen design based on feedback

### Phase 2: Backend
- [ ] Expand weather_service.py — API call, emoji mapping, caching, moon phase
- [ ] Update app.py endpoints with new response shapes
- [ ] Add temperature_unit config default

### Phase 3: Frontend
- [ ] Create shared weatherService.js module
- [ ] Build weather bottom bar (weatherBar.js + HTML + CSS)
- [ ] Enhance morning display with forecast, details, sun/moon
- [ ] Wire up app.js initialization and visibility coordination

### Phase 4: Testing
- [ ] Update integration tests for expanded weather endpoint
- [ ] Manual verification of all features
