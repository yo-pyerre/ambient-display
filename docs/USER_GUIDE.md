# User Guide

Welcome to the Raspberry Pi Art Display! This guide will help you use and manage your digital art frame.

## Overview

The Raspberry Pi Art Display is a smart digital art frame that:
- 🖼️ Shows a slideshow of your favorite images
- 👤 Detects when you're home and turns off when you're away
- ☀️🌙 Automatically switches between day and night themes
- 📝 Can display your TODO list on demand

## Daily Use

### Viewing the Slideshow

Once set up, the display will automatically:
1. Start when the Raspberry Pi boots
2. Begin cycling through images in your collection
3. Fade smoothly between images
4. Adapt to the time of day (light theme during day, dark theme at night)

### Showing TODOs

Press the **T** key on a connected keyboard to toggle the TODO list overlay.

**Tip**: You can connect a wireless keyboard for easy control from your couch!

### Away Mode

When you leave home (and your phone disconnects from WiFi), the display will:
1. Detect your absence within 1-2 minutes
2. Gradually fade to black
3. Pause the slideshow to save resources
4. Turn back on when you return

## Managing Your Content

### Adding Images

1. Connect to your Raspberry Pi via SSH or use a USB drive
2. Copy images to the `cover art/` directory:
   ```bash
   scp my-image.jpg pi@raspberrypi:~/art-display/cover\ art/
   ```
3. Supported formats: JPG, JPEG, PNG
4. Images are automatically detected - no restart needed!

**Tips**:
- Resize images to your display resolution for best performance
- Use descriptive filenames - they're sorted alphabetically
- Mix portrait and landscape orientations

### Managing TODOs

Edit the `todos.txt` file with your TODO items (one per line):

```bash
ssh pi@raspberrypi
nano ~/art-display/todos.txt
```

**Format**:
```
Complete the project report
Call dentist for appointment
Buy groceries: milk, eggs, bread
Plan weekend trip
```

**Tips**:
- Keep items short for better readability from a distance
- Updates are detected automatically within ~5 seconds
- Leave the file empty to hide the TODO display

### Removing Images

```bash
ssh pi@raspberrypi
cd ~/art-display/cover\ art
rm unwanted-image.jpg
```

## Configuration

### Changing Slideshow Speed

Edit the configuration file:
```bash
ssh pi@raspberrypi
nano ~/art-display/config/config.json
```

Change `image_duration` (in seconds):
```json
{
  "image_duration": 45
}
```

Restart the backend:
```bash
sudo systemctl restart art-display
```

### Adjusting Day/Night Times

In `config/config.json`, update:
```json
{
  "time_periods": {
    "day_start": "07:00",
    "night_start": "21:00"
  }
}
```

### Setting Your Device IP

For presence detection, set your phone's IP address in `config/config.json`:
```json
{
  "device_ip": "192.168.1.150"
}
```

**Finding your IP**:
- iPhone: Settings → WiFi → (i) → IP Address
- Android: Settings → WiFi → Advanced

## Remote Access

### SSH Access

Connect to your Raspberry Pi from another computer:

```bash
ssh pi@raspberrypi.local
# or
ssh pi@<ip-address>
```

Default password: `raspberry` (change this for security!)

### Viewing Logs

Check if everything is running correctly:

```bash
# Backend logs
sudo journalctl -u art-display -f

# System logs
tail -f ~/.xsession-errors
```

### Restarting the Display

```bash
# Restart backend only
sudo systemctl restart art-display

# Full system restart
sudo reboot
```

## Keyboard Shortcuts

When the display is active:

- **T**: Toggle TODO list overlay
- **Esc**: Exit kiosk mode (shows desktop)
- **F11**: Toggle fullscreen

## Tips & Tricks

### Best Image Practices

1. **Resolution**: Match your display resolution
   - 1920×1080 for Full HD displays
   - 1280×720 for HD displays

2. **File Size**: Compress images to < 2MB for fast loading

3. **Organization**: Use folders in `cover art/`:
   ```
   cover art/
   ├── nature/
   ├── abstract/
   └── photography/
   ```

### Optimizing Performance

1. **Fewer Images**: Keep collection under 100 images for best performance
2. **Longer Duration**: Increase `image_duration` to reduce CPU usage
3. **Network**: Use 5GHz WiFi if available

### Creating Custom TODOs

Use formatting for better readability:
```
□ Incomplete task
✓ Completed task
📅 2026-01-20: Meeting
⚠️ URGENT: Important item
```

### Setting Static IP

To ensure consistent presence detection, set a static IP for your phone:

1. In your router settings, assign a DHCP reservation
2. Or configure static IP on your device
3. Update `config/config.json` with the static IP

## Maintenance

### Weekly

- Check that images are displaying correctly
- Verify presence detection is working
- Update TODO list

### Monthly

- Update Raspberry Pi OS:
  ```bash
  sudo apt-get update && sudo apt-get upgrade
  ```
- Clean display screen
- Check disk space: `df -h`

### As Needed

- Add new images to keep content fresh
- Adjust slideshow speed based on preferences
- Update configuration for seasonal time changes

## Getting Help

1. **Check Logs**: Most issues show up in logs
   ```bash
   sudo journalctl -u art-display -f
   ```

2. **Test Backend**: Visit http://raspberrypi.local:5000/health

3. **Test Images**: Check http://raspberrypi.local:5000/api/images

4. **See Troubleshooting Guide**: `docs/TROUBLESHOOTING.md`

## Safety

- Don't leave the display on 24/7 if unattended
- Ensure proper ventilation for the Raspberry Pi
- Use a quality power supply (2.5A minimum)
- Keep software updated for security patches
