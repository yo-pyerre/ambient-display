# Raspberry Pi Art Display - Implementation Tasks

## Phase 1: Project Setup & Infrastructure

- [x] Create project directory structure (backend/, frontend/, config/, docs/)
- [x] Initialize Python virtual environment
- [x] Create requirements.txt with initial dependencies (Flask/FastAPI)
- [x] Create .gitignore file
- [x] Set up basic README.md with project description

## Phase 2: Backend - Basic Server

- [x] Create main Flask/FastAPI application file
- [x] Implement basic server with health check endpoint (GET /health)
- [x] Add static file serving for frontend assets
- [x] Test server starts and health endpoint responds
- [x] Add CORS configuration for local development

## Phase 3: Backend - Configuration Management

- [x] Create config.json structure (image_duration, device_ip, paths)
- [x] Implement configuration loader module
- [x] Add endpoint to read configuration (GET /api/config)
- [x] Test configuration can be read and modified
- [x] Add default configuration values

## Phase 4: Backend - Image File Handling

- [x] Create function to scan /cover art directory for images
- [x] Filter valid image files (JPG, PNG)
- [x] Implement endpoint to list available images (GET /api/images)
- [x] Test endpoint returns correct image paths
- [x] Add error handling for missing directory

## Phase 5: Backend - TODO File Handling

- [x] Create function to read TODO text file
- [x] Implement endpoint to get TODO list (GET /api/todos)
- [x] Test endpoint returns TODO content
- [x] Add error handling for missing TODO file
- [x] Add file watching to detect TODO changes

## Phase 6: Backend - Time-of-Day Service

- [x] Create time period detector (day/night)
- [x] Define configurable time thresholds in config
- [x] Implement endpoint to get current time period (GET /api/time-period)
- [x] Test time period detection with various times
- [x] Add timezone support

## Phase 7: Backend - Network Presence Detection

- [x] Research and choose network scanning method (arp-scan vs ping)
- [x] Implement device presence checker function
- [x] Test presence detection with target device
- [x] Create background scheduler for periodic scanning
- [x] Implement endpoint to get presence status (GET /api/presence)
- [x] Add configurable scan interval to config
- [x] Test presence status updates correctly

## Phase 8: Frontend - Basic Structure

- [x] Create index.html with basic structure
- [x] Create main CSS file with reset and base styles
- [x] Create main JavaScript module structure
- [x] Test frontend loads in browser
- [x] Add fullscreen/kiosk mode CSS

## Phase 9: Frontend - Image Slideshow

- [x] Create image container element in HTML
- [x] Implement function to fetch image list from API
- [x] Create image preloader to cache next image
- [x] Implement slideshow logic with configurable interval
- [x] Add CSS transitions for smooth image changes
- [x] Test slideshow cycles through images
- [x] Add error handling for failed image loads

## Phase 10: Frontend - TODO Display

- [ ] Create TODO overlay component in HTML
- [ ] Style TODO list for distance legibility (large font, high contrast)
- [ ] Implement function to fetch TODO data from API
- [ ] Add toggle functionality to show/hide TODO overlay
- [ ] Test TODO display renders correctly
- [ ] Add automatic line wrapping for long TODO items

## Phase 11: Frontend - State Management

- [ ] Create state manager module
- [ ] Implement polling function for presence status
- [ ] Add logic to switch between active/away states
- [ ] Test state transitions work correctly
- [ ] Add configurable poll interval
- [ ] Implement screen blanking for away state

## Phase 12: Frontend - Time-Based Behavior

- [ ] Implement polling for time period from API
- [ ] Add day/night mode CSS variables
- [ ] Create function to apply time-based styling
- [ ] Test day/night transitions
- [ ] Add smooth transitions between modes

## Phase 13: Integration Testing

- [ ] Test full flow: presence detection → display activation
- [ ] Test image slideshow runs continuously
- [ ] Test TODO overlay displays correctly
- [ ] Test time-based behavior changes
- [ ] Test configuration changes take effect
- [ ] Test system recovery from network drops

## Phase 14: System Deployment

- [ ] Create systemd service file for backend
- [ ] Test backend starts on boot
- [ ] Create startup script for Chromium kiosk mode
- [ ] Test frontend launches in kiosk mode on boot
- [ ] Configure WiFi auto-reconnect
- [ ] Test full system restart

## Phase 15: Documentation & Polish

- [ ] Document configuration file format
- [ ] Create deployment guide for Raspberry Pi
- [ ] Document SSH access and remote management
- [ ] Add troubleshooting section
- [ ] Create user guide for TODO file format

## Phase 16: Future Enhancements (Optional)

- [ ] Design Python script runner for algorithmic art
- [ ] Create sandbox environment for art scripts
- [ ] Add API endpoint to execute art scripts
- [ ] Test generated artwork displays correctly
