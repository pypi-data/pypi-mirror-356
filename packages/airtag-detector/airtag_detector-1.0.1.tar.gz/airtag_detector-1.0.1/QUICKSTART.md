# Quick Start Guide

## Apple AirTag Detector for Raspberry Pi with HomeKit Integration

This guide will help you set up and run the AirTag detector with HomeKit smart plug control on your Raspberry Pi.

### 1. Installation

Run the automated setup script:

```bash
sudo ./setup.sh
```

### 2. Configure HomeKit Integration

**IMPORTANT**: Configure HomeKit before starting the detector:

```bash
python3 setup_homekit.py
```

Follow the prompts to set up Home Assistant integration (recommended) or direct HomeKit control.

### 3. Test Your Setup

Test your Bluetooth setup:

```bash
sudo python3 test_bluetooth.py
```

### 4. Start Detection

Start the service:

```bash
sudo systemctl start airtag-detector.service
```

### 5. Monitor Activity

View real-time logs:

```bash
sudo journalctl -u airtag-detector.service -f
```

Or check the log file:

```bash
tail -f airtag_detector.log
```

### 6. Stop Detection

```bash
sudo systemctl stop airtag-detector.service
```

## What to Expect

When an AirTag is detected within ~3 feet, you'll see output like:

```
2025-06-21 10:30:15 - INFO - NEW AIRTAG DETECTED: Unknown (AA:BB:CC:DD:EE:FF) RSSI: -65 dBm
2025-06-21 10:30:15 - INFO - 🔌 Smart plug turned OFF (AirTag detected)
```

When the AirTag leaves range and after the configured delay:

```
2025-06-21 10:31:45 - INFO - No AirTags detected for 30 seconds - turning plug back on
2025-06-21 10:31:45 - INFO - 🔌 Smart plug turned ON (AirTag no longer detected)
```

## Configuration

Edit `config.py` to customize:

- `AUTO_TURN_ON_DELAY`: Seconds to wait before turning plug back on (default: 30)
- `HOME_ASSISTANT_*`: Home Assistant connection settings
- `PROXIMITY_RSSI_THRESHOLD`: Detection range (-70 dBm ≈ 3 feet)

## Troubleshooting

If you encounter issues:

1. **Permission denied**: Make sure you're running with `sudo`
2. **No Bluetooth**: Run `sudo systemctl start bluetooth`
3. **HomeKit not working**: Run `python3 setup_homekit.py` to test configuration
4. **Plug not responding**: Check Home Assistant entity ID and token
5. **No devices found**: Ensure AirTags are nearby and active
6. **Service won't start**: Check logs with `sudo systemctl status airtag-detector.service`

## Important Notes

- Detection range is approximate (RSSI-based)
- AirTags may not always be detectable due to privacy features
- Running as a service will auto-start on boot
- The plug will only turn back on after the configured delay
- Multiple AirTags detected simultaneously will keep the plug off
- Logs are rotated automatically to prevent disk space issues
