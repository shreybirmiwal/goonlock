# iPhone Camera Detector with macOS Messages

A Python script that watches your camera and sends notifications via macOS Messages app when it detects an iPhone in the view.

## Features

- 📹 **Real-time camera monitoring** using OpenCV
- 🔍 **Multi-method iPhone detection**:
  - Template matching for rectangular objects
  - Color-based detection (black, white, silver iPhones)
  - Shape-based detection with aspect ratio analysis
- 📱 **Message notifications** via macOS Messages app (iMessage/SMS)
- ⚙️ **Configurable detection settings**
- 🎯 **Optional detection area limiting**
- 📊 **Real-time visualization** with detection overlays
- 📝 **Comprehensive logging**

## Quick Start

1. **Run the setup script:**
   ```bash
   python setup.py
   ```

2. **Configure your settings:**
   - Camera index (usually 0)
   - Detection confidence threshold
   - Recipient phone number or email
   - Message service (iMessage or SMS)

3. **Run the detector:**
   ```bash
   python iphone_detector.py
   ```

## Manual Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create configuration:**
   ```bash
   cp config.json.example config.json
   # Edit config.json with your settings
   ```

3. **Run the detector:**
   ```bash
   python iphone_detector.py
   ```

## Configuration

Edit `config.json` to customize:

```json
{
    "camera_index": 0,
    "detection_confidence": 0.5,
    "notification_cooldown": 60,
    "recipient_phone_number": "+1234567890",
    "recipient_email": "example@icloud.com",
    "message_service": "iMessage",
    "detection_area": {
        "enabled": false,
        "x": 0,
        "y": 0,
        "width": 640,
        "height": 480
    }
}
```

### Configuration Options

- **camera_index**: Camera device index (0 for built-in camera)
- **detection_confidence**: Confidence threshold for detections (0.1-1.0)
- **notification_cooldown**: Seconds between message notifications
- **recipient_phone_number**: Phone number for SMS/iMessage notifications
- **recipient_email**: Email address for iMessage notifications
- **message_service**: "iMessage" or "SMS"
- **detection_area**: Optional area to limit detection to

## macOS Messages Setup

1. **Grant Permissions:**
   - Go to System Preferences > Security & Privacy > Privacy > Automation
   - Allow Terminal/your IDE to control Messages app

2. **Configure Recipients:**
   - For iMessage: Use phone numbers or email addresses
   - For SMS: Use phone numbers only
   - Add recipients in `config.json`

## Controls

- **'q'**: Quit the detector
- **'s'**: Save current frame as image

## Detection Methods

The script uses three complementary detection methods:

1. **Template Matching**: Looks for rectangular objects with iPhone-like aspect ratios
2. **Color Analysis**: Detects characteristic iPhone colors (black, white, silver)
3. **Shape Analysis**: Analyzes contours for phone-like rectangular shapes

## Logging

The script creates detailed logs in `iphone_detector.log` including:
- Detection events
- SMS notification status
- Error messages
- Performance metrics

## Troubleshooting

### Camera Issues
- Check camera permissions in System Preferences
- Try different camera indices (0, 1, 2...)
- Ensure no other applications are using the camera

### Detection Issues
- Adjust `detection_confidence` in config.json
- Use `detection_area` to limit false positives
- Ensure good lighting conditions
- Position iPhone clearly in camera view

### Messaging Issues
- Check Messages app permissions in System Preferences
- Verify recipient phone number/email format
- Ensure Messages app is signed in to your Apple ID
- Test messaging with: `python macos_messenger.py`

## Requirements

- macOS (for Messages app integration)
- Python 3.7+
- OpenCV
- NumPy
- Camera access permissions
- Messages app permissions

## License

This project is for educational and personal use. Please respect privacy and local laws when using camera monitoring software.
# goonlock
