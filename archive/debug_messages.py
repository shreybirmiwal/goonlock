#!/usr/bin/env python3
"""
Debug script for macOS Messages AppleScript issues
"""

import subprocess
import sys

def test_applescript_basic():
    """Test basic AppleScript functionality."""
    print("🧪 Testing basic AppleScript...")
    
    applescript = '''
    tell application "Messages"
        activate
        delay 1
        return "Messages app is accessible"
    end tell
    '''
    
    try:
        result = subprocess.run(
            ['osascript', '-e', applescript],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        print(f"Return code: {result.returncode}")
        print(f"Output: {result.stdout}")
        print(f"Error: {result.stderr}")
        
        return result.returncode == 0
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_services():
    """Test getting services."""
    print("\n🧪 Testing services retrieval...")
    
    applescript = '''
    tell application "Messages"
        activate
        delay 1
        set serviceList to name of every service
        return serviceList as string
    end tell
    '''
    
    try:
        result = subprocess.run(
            ['osascript', '-e', applescript],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        print(f"Return code: {result.returncode}")
        print(f"Output: {result.stdout}")
        print(f"Error: {result.stderr}")
        
        return result.returncode == 0
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_simple_message():
    """Test sending a simple message."""
    print("\n🧪 Testing simple message...")
    
    # Get phone number from user
    phone = input("Enter phone number (e.g., +15129427299): ").strip()
    if not phone:
        print("No phone number provided, skipping message test")
        return False
    
    applescript = f'''
    tell application "Messages"
        activate
        delay 2
        set targetService to 1st service whose service type = iMessage
        set targetBuddy to buddy "{phone}" of targetService
        send "Test from debug script" to targetBuddy
    end tell
    '''
    
    try:
        result = subprocess.run(
            ['osascript', '-e', applescript],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        print(f"Return code: {result.returncode}")
        print(f"Output: {result.stdout}")
        print(f"Error: {result.stderr}")
        
        return result.returncode == 0
    except Exception as e:
        print(f"Error: {e}")
        return False

def check_permissions():
    """Check if we have the right permissions."""
    print("\n🔍 Checking permissions...")
    print("Make sure you have granted the following permissions:")
    print("1. System Preferences > Security & Privacy > Privacy > Automation")
    print("2. Allow Terminal (or your IDE) to control Messages")
    print("3. System Preferences > Security & Privacy > Privacy > Accessibility")
    print("4. Allow Terminal (or your IDE) to control your computer")
    
    input("\nPress Enter when you've checked the permissions...")

def main():
    """Main debug function."""
    print("🔧 macOS Messages Debug Tool")
    print("=" * 40)
    
    # Check permissions first
    check_permissions()
    
    # Run tests
    tests = [
        ("Basic AppleScript", test_applescript_basic),
        ("Services Retrieval", test_services),
        ("Simple Message", test_simple_message)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"Test failed with error: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 40)
    print("📊 Test Results Summary:")
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {test_name}: {status}")
    
    print("\n💡 Troubleshooting Tips:")
    print("- Make sure Messages app is signed in to your Apple ID")
    print("- Check that the phone number is in the correct format (+1XXXXXXXXXX)")
    print("- Try opening Messages app manually first")
    print("- Restart Messages app if it's not responding")

if __name__ == "__main__":
    main()
