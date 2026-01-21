# Troubleshooting Guide

This guide helps you diagnose and fix common issues with the Raspberry Pi Art Display.

## Quick Diagnostics

Run these commands to check system status:

```bash
# Check backend service
sudo systemctl status art-display

# Check backend logs
sudo journalctl -u art-display -n 50

# Test backend API
curl http://localhost:5000/health

# Check images
curl http://localhost:5000/api/images

# Check disk space
df -h

# Check memory
free -h
```

## Common Issues

### Backend Won't Start

**Symptoms**: Service fails to start, browser shows connection error

**Diagnosis**:
```bash
sudo systemctl status art-display
sudo journalctl -u art-display -n 50
```

**Solutions**:

1. **Permission Error**:
   ```bash
   sudo chown -R pi:pi ~/art-display
   chmod +x ~/art-display/backend/app.py
   ```

2. **Python Dependencies Missing**:
   ```bash
   cd ~/art-display
   uv pip install -r requirements.txt
   ```

3. **Port Already in Use**:
   ```bash
   sudo lsof -i :5000
   sudo kill -9 <PID>
   ```

4. **Wrong Working Directory**:
   Check service file has correct path:
   ```bash
   sudo nano /etc/systemd/system/art-display.service
   # Verify WorkingDirectory matches your installation
   ```

### No Images Appearing

**Symptoms**: Blank screen, no images loading

**Diagnosis**:
```bash
# Check if images exist
ls -la "cover art/"

# Test API
curl http://localhost:5000/api/images

# Check backend logs
sudo journalctl -u art-display -n 50
```

**Solutions**:

1. **No Images in Directory**:
   ```bash
   cp ~/Pictures/*.jpg "cover art/"
   ```

2. **Wrong File Format**:
   - Supported: JPG, JPEG, PNG
   - Not supported: GIF, WEBP, BMP, TIFF
   ```bash
   # Convert images
   convert image.gif image.jpg
   ```

3. **Permission Error**:
   ```bash
   chmod 644 "cover art"/*
   ```

4. **Wrong Path in Config**:
   ```bash
   nano config/config.json
   # Check paths.images setting
   ```

### Kiosk Mode Won't Start

**Symptoms**: Desktop appears instead of kiosk mode

**Diagnosis**:
```bash
# Check autostart file
cat ~/.config/lxsession/LXDE-pi/autostart

# Check X server logs
cat ~/.xsession-errors
```

**Solutions**:

1. **Autostart Not Configured**:
   ```bash
   cp deployment/autostart ~/.config/lxsession/LXDE-pi/autostart
   ```

2. **Script Not Executable**:
   ```bash
   chmod +x deployment/start-kiosk.sh
   ```

3. **Chromium Not Installed**:
   ```bash
   sudo apt-get install chromium-browser
   ```

4. **Backend Not Ready**:
   Script waits 30 seconds for backend. If it takes longer:
   ```bash
   nano deployment/start-kiosk.sh
   # Increase timeout in the for loop
   ```

### Presence Detection Not Working

**Symptoms**: Display doesn't turn off when away, or doesn't turn on when home

**Diagnosis**:
```bash
# Test presence API
curl http://localhost:5000/api/presence

# Test ping manually
ping <your-device-ip>

# Check config
cat config/config.json | grep device_ip
```

**Solutions**:

1. **Wrong IP Address**:
   - Find correct IP on your device
   - Update config/config.json
   - Restart backend

2. **Device Uses Randomized MAC** (iOS/Android privacy feature):
   - Disable MAC randomization for home WiFi
   - Or set device to use static IP

3. **Firewall Blocking Ping**:
   ```bash
   # On device, allow ICMP if possible
   # Or increase scan_interval in config
   ```

4. **Network Issue**:
   ```bash
   # Verify both devices on same network
   ip addr show wlan0
   ```

### Display Blanks Randomly

**Symptoms**: Screen goes black unexpectedly

**Possible Causes**:

1. **Screen Saver Enabled**:
   ```bash
   # Disable screensaver
   xset s off
   xset -dpms
   ```

2. **Wrong Presence Detection**:
   Check if device IP is correct:
   ```bash
   curl http://localhost:5000/api/presence
   ```

3. **Power Management**:
   ```bash
   # Check HDMI status
   tvservice -s

   # Force HDMI on
   tvservice -p
   ```

### TODO List Not Showing

**Symptoms**: Press T but nothing appears

**Diagnosis**:
```bash
# Check TODO file
cat todos.txt

# Test API
curl http://localhost:5000/api/todos

# Check browser console
# Press F12 in browser to see JavaScript errors
```

**Solutions**:

1. **File Doesn't Exist**:
   ```bash
   echo "Test TODO" > todos.txt
   ```

2. **Wrong Path**:
   ```bash
   nano config/config.json
   # Check paths.todos
   ```

3. **JavaScript Error**:
   - Open browser console (F12)
   - Check for errors
   - Refresh page

### Day/Night Theme Not Switching

**Symptoms**: Theme stays the same all day

**Diagnosis**:
```bash
# Check time period API
curl http://localhost:5000/api/time-period

# Check config
cat config/config.json | grep time_periods

# Check system time
date
```

**Solutions**:

1. **Wrong System Time**:
   ```bash
   sudo timedatectl set-timezone America/New_York
   # Or your timezone
   ```

2. **Wrong Time Format**:
   Must be HH:MM (24-hour):
   ```json
   "time_periods": {
     "day_start": "06:00",
     "night_start": "22:00"
   }
   ```

3. **Frontend Not Polling**:
   Check browser console for errors

### Slow Performance

**Symptoms**: Sluggish transitions, high CPU usage

**Solutions**:

1. **Large Images**:
   ```bash
   # Resize images to display resolution
   mogrify -resize 1920x1080 "cover art"/*.jpg
   ```

2. **Too Many Images**:
   - Keep under 100 images
   - Or increase scan interval

3. **Memory Issue**:
   ```bash
   free -h
   # If low, close other applications
   ```

4. **Increase Image Duration**:
   ```json
   "image_duration": 60
   ```

5. **Slower Transitions**:
   ```json
   "display": {
     "transition_duration": 500
   }
   ```

### WiFi Disconnects

**Symptoms**: Network connection drops, presence detection fails

**Solutions**:

1. **Enable WiFi Power Management**:
   ```bash
   sudo nano /etc/rc.local
   # Add before exit 0:
   /sbin/iwconfig wlan0 power off
   ```

2. **Static IP**:
   ```bash
   sudo nano /etc/dhcpcd.conf
   # Add:
   interface wlan0
   static ip_address=192.168.1.200/24
   static routers=192.168.1.1
   static domain_name_servers=192.168.1.1
   ```

3. **Better WiFi Signal**:
   - Move Raspberry Pi closer to router
   - Use WiFi extender
   - Upgrade to 5GHz

### Browser Shows Error Page

**Symptoms**: "Unable to connect" or error page in browser

**Diagnosis**:
```bash
# Test if backend is running
curl http://localhost:5000/health

# Check if port is listening
sudo netstat -tlnp | grep 5000
```

**Solutions**:

1. **Backend Crashed**:
   ```bash
   sudo systemctl restart art-display
   ```

2. **Wrong URL**:
   Ensure kiosk script uses `http://localhost:5000`

3. **Firewall**:
   ```bash
   sudo ufw allow 5000
   ```

## Advanced Troubleshooting

### Enable Debug Logging

Edit backend service to enable debug mode:
```bash
sudo nano /etc/systemd/system/art-display.service
```

Add to `[Service]`:
```ini
Environment="FLASK_DEBUG=1"
```

Restart:
```bash
sudo systemctl daemon-reload
sudo systemctl restart art-display
```

### Testing Backend Components

```bash
cd ~/art-display

# Test image handler
uv run python -c "
from backend.image_handler import ImageHandler
h = ImageHandler('cover art')
print(h.scan_images())
"

# Test config loader
uv run python -c "
from backend.config_loader import get_config
print(get_config().get())
"

# Test presence detector
uv run python -c "
from backend.presence_detector import PresenceDetector
d = PresenceDetector('127.0.0.1')
print(d.check_presence())
"
```

### Reset Everything

If all else fails:

```bash
# Stop service
sudo systemctl stop art-display

# Remove virtual environment
rm -rf ~/art-display/.venv

# Reinstall
cd ~/art-display
uv venv
uv pip install -r requirements.txt

# Restart
sudo systemctl start art-display
```

## Getting More Help

1. **Check Logs** (most important):
   ```bash
   sudo journalctl -u art-display -f
   ```

2. **Test API Endpoints**:
   - Health: http://raspberrypi.local:5000/health
   - Config: http://raspberrypi.local:5000/api/config
   - Images: http://raspberrypi.local:5000/api/images
   - TODOs: http://raspberrypi.local:5000/api/todos
   - Time: http://raspberrypi.local:5000/api/time-period
   - Presence: http://raspberrypi.local:5000/api/presence

3. **Run Integration Tests**:
   ```bash
   cd ~/art-display
   uv run python tests/integration_test.py
   ```

4. **System Information**:
   ```bash
   uname -a
   python3 --version
   df -h
   free -h
   ```

## Prevention

- Keep system updated: `sudo apt-get update && sudo apt-get upgrade`
- Monitor disk space regularly
- Use quality SD card (avoid cheap cards)
- Ensure good power supply (2.5A+)
- Keep Raspberry Pi cool (consider heatsinks)
