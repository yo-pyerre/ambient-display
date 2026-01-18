# Specification: Raspberry Pi Art Display

## 1. Overview
The **Raspberry Pi Art Display** is a wall-mounted digital frame powered by a Raspberry Pi. Its primary purpose is to display aesthetic artwork from a local collection, enhancing the ambiance of the room. It features "smart" capabilities, including presence detection to manage power/display state, time-of-day awareness for dynamic content adaptation, and a utility mode to display a personal TODO list.

## 2. Functional Requirements

### 2.1 Artwork Display
- **Source**: The system shall read image files (JPG, PNG) from a local directory (`/cover art`).
- **Slideshow**: Images shall cycle automatically at a configurable interval.
- **Future Scope**: The system shall eventually support executing Python scripts to generate algorithmic artwork on the fly.

### 2.2 Dynamic Content (Time of Day)
- **Time Awareness**: The system shall track the local time of day.
- **Content Adaptation**: The display behavior or content selection shall adjust based on time periods (e.g., Day vs. Night). *Specific implementation details (e.g., brightness change vs. specific playlists) to be defined in implementation.*

### 2.3 Presence Detection
- **Mechanism**: The system shall scan the local network (WiFi) to detect the presence of a specific mobile device.
- **Behavior**:
    - **Home**: Display is active (Art or TODOs).
    - **Away**: Display may turn off or enter a low-power mode to save energy.

### 2.4 Dashboard & Utilities
- **TODO List**: The system shall read a local text file containing TODO items and display them as an overlay or a dedicated screen mode.
- **Overlay**: The TODO list should be legible from a distance.

### 2.5 Control & Management
- **Remote Control**: The system shall be managed remotely via SSH.
- **Configuration**: Settings (image duration, target device IP, file paths) shall be editable via configuration files accessed over SSH.

## 3. Non-Functional Requirements

### 3.1 Hardware & Environment
- **Platform**: Raspberry Pi 2.
- **Display**: Wall-mounted monitor connected via HDMI.
- **Network**: WiFi connection required for presence detection.

### 3.2 Software Architecture
- **Type**: Web Application running in Kiosk Mode.
- **Backend**: Python-based web server (e.g., Flask/FastAPI) to handle local system resources (file system, network scanning).
- **Frontend**: HTML/CSS/JavaScript for rendering the UI.
- **Browser**: Chromium (or similar) launched in full-screen kiosk mode on boot.

### 3.3 Performance
- **Responsiveness**: UI transitions should be smooth.
- **Reliability**: The system must recover automatically from network drops or minor errors without user intervention.
- **Resource Usage**: The application should be optimized to run indefinitely without memory leaks.

## 4. Architecture
The system follows a simple client-server model running locally on the Pi.

### 4.1 Backend (Python)
- **API Server**: Serves the frontend assets and provides endpoints for data.
- **Scanner Service**: Background process that periodically scans the network (ARP-scan or ping) for the user's device.
- **File Handler**: Reads the `cover art/` directory and the TODO text file.

### 4.2 Frontend (Web)
- **Art View**: Full-screen image component with transitions.
- **Dashboard View**: Text-based component for the TODO list.
- **State Manager**: Polls the backend for presence status and content updates.

## 5. Dependencies
- **OS**: Raspberry Pi OS (Lite or Desktop).
- **Runtime**: Python 3.x.
- **Libraries**:
    - Web Framework: `Flask` or `FastAPI`.
    - Network: `scapy` or system `arp-scan` utility.
- **Browser**: Chromium.
