# goonlock

Phone Camera Detector with macOS Messages - A script that watches your camera and randomly sends custom messages to different people when it detects a phone using YOLOv8.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure settings:**
   ```bash
   python3 config_gui.py
   ```
   Or edit `config.json` manually.

3. **Run the detector:**
   ```bash
   python3 iphone_detector.py
   ```

## Files

- `iphone_detector.py` - Main detection script
- `config_gui.py` - Configuration GUI
- `macos_messenger.py` - Messages integration
- `config.json` - Configuration settings
- `requirements.txt` - Python dependencies
- `archive/` - Setup and test utilities

## Configuration

Use the GUI: `python3 config_gui.py`

Or edit `config.json` manually:
```json
{
    "camera_index": 0,
    "detection_confidence": 0.5,
    "notification_cooldown": 60,
    "recipients": [
        {
            "name": "Mom",
            "phone": "+1234567890",
            "message": "I'm on my phone while working!"
        },
        {
            "name": "My Ex",
            "phone": "+1987654321",
            "message": "I LOVE U"
        }
    ]
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