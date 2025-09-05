#!/usr/bin/env python3
"""
Setup script for iPhone Camera Detector
"""

import subprocess
import sys
import os
import json

def install_requirements():
    """Install required packages."""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False

def create_config():
    """Create configuration file with user input."""
    print("\n📱 iPhone Camera Detector Setup")
    print("=" * 40)
    
    # Check if config already exists
    if os.path.exists("config.json"):
        response = input("Configuration file already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Keeping existing configuration.")
            return True
    
    print("\n🔧 Camera Configuration:")
    camera_index = input("Camera index (usually 0 for built-in camera): ").strip() or "0"
    
    print("\n📊 Detection Settings:")
    confidence = input("Detection confidence threshold (0.1-1.0, default 0.5): ").strip() or "0.5"
    cooldown = input("Notification cooldown in seconds (default 60): ").strip() or "60"
    
    print("\n📱 macOS Messages Configuration:")
    print("(Messages will be sent from your Apple account)")
    recipient_phone = input("Recipient phone number (+1234567890) or email: ").strip()
    recipient_email = input("Recipient email (optional, for iMessage): ").strip()
    
    print("\nChoose messaging service:")
    print("1. iMessage (recommended, works with phone numbers and emails)")
    print("2. SMS (requires phone number)")
    service_choice = input("Enter choice (1 or 2, default 1): ").strip() or "1"
    message_service = "iMessage" if service_choice == "1" else "SMS"
    
    print("\n🎯 Detection Area (optional):")
    use_area = input("Use specific detection area? (y/N): ").strip().lower() == 'y'
    
    detection_area = {
        "enabled": False,
        "x": 0,
        "y": 0,
        "width": 640,
        "height": 480
    }
    
    if use_area:
        detection_area["enabled"] = True
        detection_area["x"] = int(input("X coordinate (default 0): ").strip() or "0")
        detection_area["y"] = int(input("Y coordinate (default 0): ").strip() or "0")
        detection_area["width"] = int(input("Width (default 640): ").strip() or "640")
        detection_area["height"] = int(input("Height (default 480): ").strip() or "480")
    
    # Create config
    config = {
        "camera_index": int(camera_index),
        "detection_confidence": float(confidence),
        "notification_cooldown": int(cooldown),
        "recipient_phone_number": recipient_phone,
        "recipient_email": recipient_email,
        "message_service": message_service,
        "detection_area": detection_area
    }
    
    try:
        with open("config.json", "w") as f:
            json.dump(config, f, indent=4)
        print("✅ Configuration saved to config.json")
        return True
    except Exception as e:
        print(f"❌ Error saving configuration: {e}")
        return False

def test_camera():
    """Test camera access."""
    print("\n📹 Testing camera access...")
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print("✅ Camera is working!")
                cap.release()
                return True
            else:
                print("❌ Camera opened but couldn't read frame")
                cap.release()
                return False
        else:
            print("❌ Could not open camera")
            return False
    except ImportError:
        print("❌ OpenCV not installed")
        return False
    except Exception as e:
        print(f"❌ Camera test failed: {e}")
        return False

def main():
    """Main setup function."""
    print("🚀 iPhone Camera Detector Setup")
    print("=" * 40)
    
    # Install requirements
    if not install_requirements():
        print("Setup failed at requirements installation.")
        return False
    
    # Test camera
    if not test_camera():
        print("⚠️  Camera test failed. You may need to check camera permissions.")
    
    # Create configuration
    if not create_config():
        print("Setup failed at configuration creation.")
        return False
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Grant Messages app permissions:")
    print("   - Go to System Preferences > Security & Privacy > Privacy > Automation")
    print("   - Allow Terminal/your IDE to control Messages")
    print("2. Test messaging: python macos_messenger.py")
    print("3. Run the detector: python iphone_detector.py")
    print("4. Press 'q' to quit, 's' to save a frame")
    print("\n💡 Tips:")
    print("- Adjust detection_confidence in config.json if needed")
    print("- Use detection_area to limit detection to a specific region")
    print("- Check iphone_detector.log for detailed logs")
    print("- iMessage works with phone numbers and email addresses")
    print("- SMS only works with phone numbers")
    
    return True

if __name__ == "__main__":
    main()
