#!/usr/bin/env python3
"""
Test script to verify iPhone detector setup
"""

import sys
import importlib

def test_imports():
    """Test if all required packages can be imported."""
    packages = [
        ('cv2', 'opencv-python'),
        ('numpy', 'numpy')
    ]
    
    print("Testing package imports...")
    all_good = True
    
    for package, pip_name in packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package} imported successfully")
        except ImportError:
            print(f"❌ {package} not found. Install with: pip install {pip_name}")
            all_good = False
    
    return all_good

def test_camera():
    """Test camera access."""
    try:
        import cv2
        print("\nTesting camera access...")
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print("✅ Camera is working!")
                print(f"   Frame shape: {frame.shape}")
                cap.release()
                return True
            else:
                print("❌ Camera opened but couldn't read frame")
                cap.release()
                return False
        else:
            print("❌ Could not open camera")
            return False
    except Exception as e:
        print(f"❌ Camera test failed: {e}")
        return False

def test_config():
    """Test configuration file."""
    import os
    import json
    
    print("\nTesting configuration...")
    if os.path.exists("config.json"):
        try:
            with open("config.json", "r") as f:
                config = json.load(f)
            print("✅ Configuration file found and valid")
            
            # Check required fields
            required_fields = [
                "camera_index", "detection_confidence", "notification_cooldown",
                "message_service"
            ]
            
            # Check that at least one recipient is configured
            has_recipient = (config.get("recipient_phone_number") or 
                           config.get("recipient_email"))
            
            missing_fields = []
            for field in required_fields:
                if field not in config:
                    missing_fields.append(field)
                elif field == "camera_index" and config[field] is None:
                    missing_fields.append(field)
                elif field != "camera_index" and not config[field]:
                    missing_fields.append(field)
            
            if not has_recipient:
                missing_fields.append("recipient (phone or email)")
            
            if missing_fields:
                print(f"⚠️  Missing or empty fields: {', '.join(missing_fields)}")
                return False
            else:
                print("✅ All required configuration fields present")
                return True
                
        except Exception as e:
            print(f"❌ Error reading config: {e}")
            return False
    else:
        print("❌ Configuration file not found. Run setup.py first.")
        return False

def test_macos_messaging():
    """Test macOS messaging functionality."""
    try:
        from macos_messenger import MacOSMessenger
        print("\nTesting macOS messaging...")
        
        messenger = MacOSMessenger()
        
        # Check permissions
        if messenger.check_messages_permissions():
            print("✅ Messages app permissions look good")
        else:
            print("❌ Messages app permissions may be insufficient")
            print("   Go to System Preferences > Security & Privacy > Privacy > Automation")
            print("   Make sure Terminal/IDE has permission to control Messages")
            return False
        
        # Get available services
        services = messenger.get_available_services()
        if services:
            print(f"✅ Available services: {', '.join(services)}")
        else:
            print("⚠️  No messaging services found")
        
        return True
        
    except ImportError:
        print("❌ macOS messenger module not found")
        return False
    except Exception as e:
        print(f"❌ macOS messaging test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 iPhone Detector Setup Test (macOS)")
    print("=" * 40)
    
    tests = [
        ("Package Imports", test_imports),
        ("Camera Access", test_camera),
        ("Configuration", test_config),
        ("macOS Messaging", test_macos_messaging)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}:")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with error: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 40)
    print("📊 Test Results:")
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 All tests passed! You're ready to run the detector.")
        print("   Run: python iphone_detector.py")
        print("   Test messaging: python macos_messenger.py")
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
        print("   Run: python setup.py to reconfigure")
        print("   Grant Messages permissions in System Preferences if needed")

if __name__ == "__main__":
    main()
