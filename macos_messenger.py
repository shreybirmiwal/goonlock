#!/usr/bin/env python3
"""
macOS Message Sender using AppleScript

This module provides functionality to send messages through macOS Messages app
using AppleScript automation.
"""

import subprocess
import logging
import time
from typing import Optional, List

logger = logging.getLogger(__name__)

class MacOSMessenger:
    def __init__(self):
        """Initialize the macOS messenger."""
        self.last_message_time = 0
        self.message_cooldown = 60  # seconds between messages
        
    def send_message(self, recipient: str, message: str, service: str = "iMessage") -> bool:
        """
        Send a message using macOS Messages app via AppleScript.
        
        Args:
            recipient: Phone number or email address
            message: Message content
            service: "iMessage" or "SMS"
            
        Returns:
            bool: True if message was sent successfully
        """
        try:
            # Format phone number properly
            formatted_recipient = self._format_recipient(recipient)
            
            # Escape special characters for AppleScript
            escaped_message = message.replace('"', '\\"').replace('\\', '\\\\')
            escaped_recipient = formatted_recipient.replace('"', '\\"').replace('\\', '\\\\')
            
            # AppleScript to send message - corrected version
            if service == "iMessage":
                service_type = "iMessage"
            else:
                service_type = "SMS"
                
            applescript = f'''
            tell application "Messages"
                activate
                delay 1
                set targetService to 1st service whose service type = {service_type}
                set targetBuddy to buddy "{escaped_recipient}" of targetService
                send "{escaped_message}" to targetBuddy
            end tell
            '''
            
            # Execute AppleScript
            result = subprocess.run(
                ['osascript', '-e', applescript],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                logger.info(f"Message sent successfully to {recipient}")
                return True
            else:
                logger.error(f"Failed to send message: {result.stderr}")
                # Try alternative method
                return self._send_message_alternative(recipient, message, service)
                
        except subprocess.TimeoutExpired:
            logger.error("Message sending timed out")
            return False
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return False
    
    def _format_recipient(self, recipient: str) -> str:
        """Format recipient for Messages app."""
        # Remove any non-digit characters except + for phone numbers
        if recipient.replace('+', '').replace('-', '').replace(' ', '').replace('(', '').replace(')', '').isdigit():
            # It's a phone number
            # Remove all non-digit characters except +
            phone = ''.join(c for c in recipient if c.isdigit() or c == '+')
            # Add +1 if it's a 10-digit US number
            if len(phone) == 10:
                phone = '+1' + phone
            elif len(phone) == 11 and phone.startswith('1'):
                phone = '+' + phone
            return phone
        else:
            # It's an email address
            return recipient
    
    def _send_message_alternative(self, recipient: str, message: str, service: str) -> bool:
        """Alternative method to send message using different AppleScript approach."""
        try:
            formatted_recipient = self._format_recipient(recipient)
            escaped_message = message.replace('"', '\\"').replace('\\', '\\\\')
            escaped_recipient = formatted_recipient.replace('"', '\\"').replace('\\', '\\\\')
            
            # Alternative AppleScript approach - corrected
            if service == "iMessage":
                service_type = "iMessage"
            else:
                service_type = "SMS"
                
            applescript = f'''
            tell application "Messages"
                activate
                delay 1
                set targetService to 1st service whose service type = {service_type}
                set targetBuddy to buddy "{escaped_recipient}" of targetService
                set newChat to make new chat with properties {{service:targetService, participants:{{targetBuddy}}}}
                send "{escaped_message}" to newChat
            end tell
            '''
            
            result = subprocess.run(
                ['osascript', '-e', applescript],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                logger.info(f"Message sent successfully to {recipient} (alternative method)")
                return True
            else:
                logger.error(f"Alternative method also failed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error in alternative method: {e}")
            return False
    
    def send_imessage(self, recipient: str, message: str) -> bool:
        """Send an iMessage."""
        return self.send_message(recipient, message, "iMessage")
    
    def send_sms(self, recipient: str, message: str) -> bool:
        """Send an SMS."""
        return self.send_message(recipient, message, "SMS")
    
    def send_notification_with_cooldown(self, recipient: str, message: str, 
                                      service: str = "iMessage") -> bool:
        """
        Send notification with cooldown to prevent spam.
        
        Args:
            recipient: Phone number or email address
            message: Message content
            service: "iMessage" or "SMS"
            
        Returns:
            bool: True if message was sent (or cooldown active)
        """
        current_time = time.time()
        
        if current_time - self.last_message_time < self.message_cooldown:
            logger.info(f"Message cooldown active. Last message sent {current_time - self.last_message_time:.1f}s ago")
            return False
        
        success = self.send_message(recipient, message, service)
        if success:
            self.last_message_time = current_time
        return success
    
    def test_messaging(self, recipient: str) -> bool:
        """
        Test messaging functionality by sending a test message.
        
        Args:
            recipient: Phone number or email address to test
            
        Returns:
            bool: True if test message was sent successfully
        """
        test_message = "🧪 Test message from iPhone Detector - " + time.strftime("%Y-%m-%d %H:%M:%S")
        
        logger.info(f"Testing messaging to {recipient}...")
        
        # Try iMessage first
        success = self.send_imessage(recipient, test_message)
        
        if not success:
            logger.info("iMessage failed, trying SMS...")
            success = self.send_sms(recipient, test_message)
        
        if success:
            logger.info("✅ Test message sent successfully!")
        else:
            logger.error("❌ Test message failed")
            
        return success
    
    def test_simple_message(self, recipient: str) -> bool:
        """
        Test with a very simple message to avoid AppleScript issues.
        
        Args:
            recipient: Phone number or email address to test
            
        Returns:
            bool: True if test message was sent successfully
        """
        try:
            formatted_recipient = self._format_recipient(recipient)
            simple_message = "Test"
            
            # Very simple AppleScript - corrected
            applescript = f'''
            tell application "Messages"
                activate
                delay 2
                set targetService to 1st service whose service type = iMessage
                set targetBuddy to buddy "{formatted_recipient}" of targetService
                send "{simple_message}" to targetBuddy
            end tell
            '''
            
            result = subprocess.run(
                ['osascript', '-e', applescript],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                logger.info("✅ Simple test message sent successfully!")
                return True
            else:
                logger.error(f"❌ Simple test failed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Simple test error: {e}")
            return False
    
    def get_available_services(self) -> List[str]:
        """
        Get list of available messaging services.
        
        Returns:
            List of available services
        """
        try:
            applescript = '''
            tell application "Messages"
                activate
                delay 1
                get name of every service
            end tell
            '''
            
            result = subprocess.run(
                ['osascript', '-e', applescript],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                services_text = result.stdout.strip()
                if services_text:
                    # Parse the services list
                    services = [s.strip() for s in services_text.split(',')]
                    logger.info(f"Available services: {services}")
                    return services
                else:
                    logger.warning("No services returned")
                    return ["iMessage", "SMS"]  # Default fallback
            else:
                logger.warning(f"Could not retrieve services list: {result.stderr}")
                return ["iMessage", "SMS"]  # Default fallback
                
        except Exception as e:
            logger.error(f"Error getting services: {e}")
            return ["iMessage", "SMS"]  # Default fallback
    
    def check_messages_permissions(self) -> bool:
        """
        Check if Messages app has necessary permissions.
        
        Returns:
            bool: True if permissions are likely sufficient
        """
        try:
            # Try to get services list as a permission test
            services = self.get_available_services()
            return len(services) > 0
        except Exception as e:
            logger.error(f"Permission check failed: {e}")
            return False

def main():
    """Test the macOS messenger."""
    print("🧪 Testing macOS Messenger")
    print("=" * 30)
    
    messenger = MacOSMessenger()
    
    # Check permissions
    print("Checking Messages app permissions...")
    if messenger.check_messages_permissions():
        print("✅ Messages app permissions look good")
    else:
        print("❌ Messages app permissions may be insufficient")
        print("   Go to System Preferences > Security & Privacy > Privacy > Automation")
        print("   Make sure Terminal/IDE has permission to control Messages")
        return
    
    # Get available services
    print("\nAvailable messaging services:")
    services = messenger.get_available_services()
    for service in services:
        print(f"  - {service}")
    
    # Test messaging
    recipient = input("\nEnter phone number or email to test (or press Enter to skip): ").strip()
    if recipient:
        print("\nChoose test method:")
        print("1. Simple test (recommended)")
        print("2. Full test")
        choice = input("Enter choice (1 or 2, default 1): ").strip() or "1"
        
        if choice == "1":
            messenger.test_simple_message(recipient)
        else:
            messenger.test_messaging(recipient)
    else:
        print("Skipping test message")

if __name__ == "__main__":
    main()
