# goonlock

Phone Camera Detector with macOS Messages - A simple script that watches your camera and sends notifications when it detects a phone using YOLOv8.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure settings:**
   Edit `config.json` with your phone number and preferences.

3. **Run the detector:**
   ```bash
   python3 iphone_detector.py
   ```

## Files

- `iphone_detector.py` - Main detection script
- `macos_messenger.py` - Messages integration
- `config.json` - Configuration settings
- `requirements.txt` - Python dependencies
- `archive/` - Setup and test utilities

## Configuration

Edit `config.json`:
```json
{
    "camera_index": 0,
    "detection_confidence": 0.5,
    "notification_cooldown": 60,
    "recipient_phone_number": "+1234567890",
    "message_service": "iMessage"
}
```

## Requirements

- macOS (for Messages app)
- Python 3.7+
- OpenCV
- NumPy
- YOLOv8 (Ultralytics)
- Messages app permissions

## Setup

1. Grant Messages app permissions in System Preferences > Security & Privacy > Privacy > Automation
2. Send a test message manually to your recipient first
3. Run the detector

## Controls

- Press `q` to quit
- Press `s` to save current frame