# Configuration Guide

This document explains all configuration options for the Raspberry Pi Art Display.

## Configuration File Location

The main configuration file is located at:
```
config/config.json
```

## Configuration Format

The configuration file uses JSON format. Here's the complete structure with explanations:

```json
{
  "image_duration": 30,
  "device_ip": "192.168.1.100",
  "paths": {
    "images": "cover art",
    "todos": "todos.txt"
  },
  "time_periods": {
    "day_start": "06:00",
    "night_start": "22:00"
  },
  "presence": {
    "scan_interval": 60,
    "scan_method": "ping"
  },
  "display": {
    "transition_duration": 1000,
    "poll_interval": 5000
  }
}
```

## Configuration Options

### Image Duration

**Key**: `image_duration`
**Type**: Number (seconds)
**Default**: 30
**Description**: How long each image is displayed before transitioning to the next one.

**Example**:
```json
"image_duration": 45
```

### Device IP

**Key**: `device_ip`
**Type**: String (IP address)
**Default**: "192.168.1.100"
**Description**: The IP address of your mobile device or computer used for presence detection. The system will ping this device to determine if you're home.

**How to find your device's IP**:
- **iOS**: Settings → WiFi → (i) icon → IP Address
- **Android**: Settings → WiFi → Advanced → IP Address
- **Computer**: Run `ipconfig` (Windows) or `ifconfig` (Mac/Linux)

**Example**:
```json
"device_ip": "192.168.1.150"
```

### Paths

**Key**: `paths`
**Type**: Object
**Description**: File and directory paths used by the application.

#### Images Path

**Key**: `paths.images`
**Type**: String (relative or absolute path)
**Default**: "cover art"
**Description**: Directory containing image files for the slideshow.

**Supported formats**: JPG, JPEG, PNG

**Example**:
```json
"paths": {
  "images": "/home/pi/my-images"
}
```

#### TODOs Path

**Key**: `paths.todos`
**Type**: String (relative or absolute path)
**Default**: "todos.txt"
**Description**: Text file containing TODO items (one per line).

**Example**:
```json
"paths": {
  "todos": "/home/pi/my-todos.txt"
}
```

### Time Periods

**Key**: `time_periods`
**Type**: Object
**Description**: Defines when day and night periods begin for theme switching.

#### Day Start

**Key**: `time_periods.day_start`
**Type**: String (HH:MM format, 24-hour)
**Default**: "06:00"
**Description**: Time when day mode begins. Display will use light theme.

**Example**:
```json
"time_periods": {
  "day_start": "07:30"
}
```

#### Night Start

**Key**: `time_periods.night_start`
**Type**: String (HH:MM format, 24-hour)
**Default**: "22:00"
**Description**: Time when night mode begins. Display will use dark theme.

**Example**:
```json
"time_periods": {
  "night_start": "20:00"
}
```

### Presence Detection

**Key**: `presence`
**Type**: Object
**Description**: Settings for device presence detection.

#### Scan Interval

**Key**: `presence.scan_interval`
**Type**: Number (seconds)
**Default**: 60
**Description**: How often to check if the device is present on the network.

**Recommendations**:
- Lower values (30-60s) = More responsive but uses more resources
- Higher values (120-300s) = Less responsive but more efficient

**Example**:
```json
"presence": {
  "scan_interval": 45
}
```

#### Scan Method

**Key**: `presence.scan_method`
**Type**: String
**Default**: "ping"
**Options**: "ping"
**Description**: Method used to detect device presence. Currently only "ping" is supported.

### Display Settings

**Key**: `display`
**Type**: Object
**Description**: Frontend display and timing settings.

#### Transition Duration

**Key**: `display.transition_duration`
**Type**: Number (milliseconds)
**Default**: 1000
**Description**: Duration of fade transitions between images.

**Example**:
```json
"display": {
  "transition_duration": 1500
}
```

#### Poll Interval

**Key**: `display.poll_interval`
**Type**: Number (milliseconds)
**Default**: 5000
**Description**: How often the frontend polls the backend for updates (presence, time period, TODOs).

**Example**:
```json
"display": {
  "poll_interval": 3000
}
```

## Reloading Configuration

After editing the configuration file:

1. **Backend changes** (image_duration, device_ip, paths, time_periods, presence):
   ```bash
   sudo systemctl restart art-display
   ```

2. **Frontend changes** (display settings):
   Refresh the browser or restart kiosk mode.

## Configuration Examples

### Minimal Configuration

```json
{
  "image_duration": 30,
  "device_ip": "192.168.1.100",
  "paths": {
    "images": "cover art",
    "todos": "todos.txt"
  },
  "time_periods": {
    "day_start": "06:00",
    "night_start": "22:00"
  },
  "presence": {
    "scan_interval": 60,
    "scan_method": "ping"
  },
  "display": {
    "transition_duration": 1000,
    "poll_interval": 5000
  }
}
```

### Fast Slideshow

```json
{
  "image_duration": 10,
  "display": {
    "transition_duration": 500
  }
}
```

### Slow Slideshow

```json
{
  "image_duration": 120,
  "display": {
    "transition_duration": 2000
  }
}
```

### Night Owl Mode

```json
{
  "time_periods": {
    "day_start": "10:00",
    "night_start": "02:00"
  }
}
```

### Aggressive Presence Detection

```json
{
  "presence": {
    "scan_interval": 30
  },
  "display": {
    "poll_interval": 2000
  }
}
```

## Validation

The application will use default values if configuration is missing or invalid. Check the backend logs for configuration errors:

```bash
sudo journalctl -u art-display -f
```

## Environment Variables

You can also set configuration via environment variables (takes precedence over config file):

```bash
export ART_DISPLAY_DEVICE_IP="192.168.1.150"
export ART_DISPLAY_IMAGE_DURATION="45"
```
