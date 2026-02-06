#!/bin/bash
# Raspberry Pi Art Display - Chromium Kiosk Mode Startup Script

# Wait for the backend to be ready
echo "Waiting for backend to start..."
for i in {1..30}; do
    if curl -s http://localhost:5000/health > /dev/null 2>&1; then
        echo "Backend is ready!"
        break
    fi
    sleep 1
done

# Disable screen blanking
xset s off
xset -dpms
xset s noblank

# Hide mouse cursor after 1 second of inactivity
unclutter -idle 1 &

# Start Chromium in kiosk mode
chromium \
    --noerrdialogs \
    --disable-infobars \
    --kiosk \
    --incognito \
    --disable-session-crashed-bubble \
    --disable-component-update \
    http://localhost:5000
