# Raspberry Pi Art Display - Deployment Guide

This guide walks you through deploying the Art Display on a Raspberry Pi.

## Prerequisites

- Raspberry Pi 2 or newer
- Raspberry Pi OS (Desktop version recommended for kiosk mode)
- HDMI-compatible display
- WiFi connection configured

## Installation Steps

### 1. Clone or Copy the Project

```bash
cd /home/pi
git clone <repository-url> art-display
# OR copy the project files to /home/pi/art-display
```

### 2. Install System Dependencies

```bash
sudo apt-get update
sudo apt-get install -y \
    python3-pip \
    python3-venv \
    chromium-browser \
    unclutter \
    x11-xserver-utils
```

### 3. Set Up Python Environment

```bash
cd /home/pi/ambient-display

# Create virtual environment and install dependencies
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Configure the Application

Edit the configuration file:

```bash
nano config/config.json
```

Update these values:
- `device_ip`: Your phone/device IP address for presence detection
- `image_duration`: Slideshow interval in seconds
- `paths.images`: Path to your image directory
- `paths.todos`: Path to your TODO file
- `time_periods`: Day/night start times

### 5. Add Your Artwork

Copy your images to the artwork directory:

```bash
cp ~/my-images/*.jpg "cover art/"
cp ~/my-images/*.png "cover art/"
```

### 6. Create TODO File (Optional)

```bash
nano todos.txt
```

Add your TODO items, one per line.

### 7. Set Up Backend Service

Install the systemd service:

```bash
# Copy service file
sudo cp deployment/art-display.service /etc/systemd/system/

# Update paths in service file if needed
sudo nano /etc/systemd/system/art-display.service

# Enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable art-display
sudo systemctl start art-display

# Check status
sudo systemctl status art-display
```

### 8. Set Up Kiosk Mode

Make the kiosk script executable:

```bash
chmod +x deployment/start-kiosk.sh
```

#### For Automatic Startup (Desktop Environment)

```bash
# Create autostart directory
mkdir -p ~/.config/lxsession/LXDE-pi

# Copy autostart configuration
cp deployment/autostart ~/.config/lxsession/LXDE-pi/autostart
```

#### For Manual Testing

```bash
# Start X server if not already running
startx

# Or just run the kiosk script
./deployment/start-kiosk.sh
```

### 9. Configure WiFi Auto-Reconnect

Edit wpa_supplicant configuration:

```bash
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```

Add or update your network:

```
network={
    ssid="YourWiFiName"
    psk="YourPassword"
    priority=1
    id_str="home"
}
```

Enable WiFi reconnect service:

```bash
sudo systemctl enable wpa_supplicant
```

### 10. Test the System

Reboot to test everything starts automatically:

```bash
sudo reboot
```

After reboot:
1. Backend should start automatically (check with `systemctl status art-display`)
2. Chromium should open in kiosk mode
3. Images should start cycling
4. Press 'T' to toggle TODO overlay

## Troubleshooting

### Backend Not Starting

Check service logs:
```bash
sudo journalctl -u art-display -f
```

### Kiosk Mode Not Starting

Check X server logs:
```bash
cat ~/.xsession-errors
```

### Images Not Loading

Check permissions:
```bash
ls -la "cover art/"
```

### Presence Detection Not Working

Test ping manually:
```bash
ping <your-device-ip>
```

## Maintenance

### View Backend Logs

```bash
sudo journalctl -u art-display -f
```

### Restart Backend

```bash
sudo systemctl restart art-display
```

### Update Configuration

```bash
nano config/config.json
sudo systemctl restart art-display
```

### Add More Images

```bash
cp new-images/*.jpg "cover art/"
# No restart needed - images are scanned periodically
```

### Update TODO List

```bash
nano todos.txt
# Changes are picked up automatically
```

## Performance Tips

1. **Image Size**: Resize images to display resolution for faster loading
2. **Memory**: Close unnecessary services to free RAM
3. **Network**: Use 5GHz WiFi for better performance
4. **Overclocking**: Consider modest overclocking for smoother transitions

## Security Notes

- Backend runs on localhost:5000 only
- No external network access required except for presence detection
- Consider firewall rules if exposing the service
- Keep Raspberry Pi OS updated

## Uninstall

```bash
# Stop and disable service
sudo systemctl stop art-display
sudo systemctl disable art-display
sudo rm /etc/systemd/system/art-display.service
sudo systemctl daemon-reload

# Remove autostart
rm ~/.config/lxsession/LXDE-pi/autostart

# Remove project
rm -rf /home/pi/art-display
```
