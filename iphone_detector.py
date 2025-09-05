#!/usr/bin/env python3
"""
iPhone Camera Detector with SMS Notifications

This script watches your camera and sends a text message when it detects an iPhone.
"""

import cv2
import numpy as np
import time
import logging
from datetime import datetime
import json
import os
from typing import Optional, Tuple
from macos_messenger import MacOSMessenger

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('iphone_detector.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class iPhoneDetector:
    def __init__(self, config_file: str = "config.json"):
        """Initialize the iPhone detector with configuration."""
        self.config = self.load_config(config_file)
        self.camera = None
        self.detection_count = 0
        self.last_notification_time = 0
        self.notification_cooldown = 60  # seconds between notifications
        
        # Initialize macOS messenger
        self.messenger = MacOSMessenger()
        self.messenger.message_cooldown = self.config.get('notification_cooldown', 60)
        
        # Check messaging permissions
        if not self.messenger.check_messages_permissions():
            logger.warning("Messages app permissions may be insufficient. Check System Preferences > Security & Privacy > Privacy > Automation")
    
    def load_config(self, config_file: str) -> dict:
        """Load configuration from JSON file."""
        default_config = {
            "camera_index": 0,
            "detection_confidence": 0.5,
            "notification_cooldown": 60,
            "recipient_phone_number": "",
            "recipient_email": "",
            "message_service": "iMessage",  # "iMessage" or "SMS"
            "detection_area": {
                "enabled": False,
                "x": 0,
                "y": 0,
                "width": 640,
                "height": 480
            }
        }
        
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                # Merge with defaults
                for key, value in default_config.items():
                    if key not in config:
                        config[key] = value
                return config
            except Exception as e:
                logger.error(f"Error loading config: {e}")
                return default_config
        else:
            # Create default config file
            with open(config_file, 'w') as f:
                json.dump(default_config, f, indent=4)
            logger.info(f"Created default config file: {config_file}")
            return default_config
    
    def initialize_camera(self) -> bool:
        """Initialize the camera."""
        try:
            self.camera = cv2.VideoCapture(self.config['camera_index'])
            if not self.camera.isOpened():
                logger.error(f"Could not open camera {self.config['camera_index']}")
                return False
            
            # Set camera properties
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.camera.set(cv2.CAP_PROP_FPS, 30)
            
            logger.info("Camera initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Error initializing camera: {e}")
            return False
    
    def detect_iphone(self, frame: np.ndarray) -> Tuple[bool, float, Tuple[int, int, int, int]]:
        """
        Detect iPhone in the frame using multiple methods.
        Returns: (detected, confidence, bounding_box)
        """
        # Method 1: Template matching for iPhone-like objects
        iphone_detected, confidence1, bbox1 = self.template_matching_detection(frame)
        
        # Method 2: Color-based detection (iPhone's characteristic colors)
        color_detected, confidence2, bbox2 = self.color_based_detection(frame)
        
        # Method 3: Shape-based detection (rectangular objects with specific aspect ratios)
        shape_detected, confidence3, bbox3 = self.shape_based_detection(frame)
        
        # Combine results
        detections = []
        if iphone_detected and confidence1 > self.config['detection_confidence']:
            detections.append((confidence1, bbox1))
        if color_detected and confidence2 > self.config['detection_confidence']:
            detections.append((confidence2, bbox2))
        if shape_detected and confidence3 > self.config['detection_confidence']:
            detections.append((confidence3, bbox3))
        
        if detections:
            # Return the detection with highest confidence
            best_confidence, best_bbox = max(detections, key=lambda x: x[0])
            return True, best_confidence, best_bbox
        
        return False, 0.0, (0, 0, 0, 0)
    
    def template_matching_detection(self, frame: np.ndarray) -> Tuple[bool, float, Tuple[int, int, int, int]]:
        """Detect iPhone using template matching."""
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Look for rectangular objects that could be phones
            # This is a simplified approach - in practice, you'd want a trained model
            edges = cv2.Canny(gray, 50, 150)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                # Approximate the contour
                epsilon = 0.02 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                
                # Check if it's roughly rectangular (4 corners)
                if len(approx) == 4:
                    x, y, w, h = cv2.boundingRect(contour)
                    aspect_ratio = w / h
                    
                    # iPhone-like aspect ratio (roughly 0.5 to 0.6)
                    if 0.4 <= aspect_ratio <= 0.7 and w > 50 and h > 80:
                        # Check if it's in the detection area if specified
                        if self.is_in_detection_area(x, y, w, h):
                            return True, 0.6, (x, y, w, h)
            
            return False, 0.0, (0, 0, 0, 0)
        except Exception as e:
            logger.error(f"Error in template matching: {e}")
            return False, 0.0, (0, 0, 0, 0)
    
    def color_based_detection(self, frame: np.ndarray) -> Tuple[bool, float, Tuple[int, int, int, int]]:
        """Detect iPhone using color analysis."""
        try:
            # Convert to HSV for better color detection
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # Define ranges for iPhone colors (black, white, silver, gold)
            # Black iPhones
            lower_black = np.array([0, 0, 0])
            upper_black = np.array([180, 255, 50])
            black_mask = cv2.inRange(hsv, lower_black, upper_black)
            
            # White iPhones
            lower_white = np.array([0, 0, 200])
            upper_white = np.array([180, 30, 255])
            white_mask = cv2.inRange(hsv, lower_white, upper_white)
            
            # Silver/Gray iPhones
            lower_silver = np.array([0, 0, 100])
            upper_silver = np.array([180, 30, 200])
            silver_mask = cv2.inRange(hsv, lower_silver, upper_silver)
            
            # Combine masks
            combined_mask = cv2.bitwise_or(black_mask, cv2.bitwise_or(white_mask, silver_mask))
            
            # Find contours
            contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 1000:  # Minimum area threshold
                    x, y, w, h = cv2.boundingRect(contour)
                    aspect_ratio = w / h
                    
                    # Check for phone-like aspect ratio
                    if 0.4 <= aspect_ratio <= 0.7:
                        if self.is_in_detection_area(x, y, w, h):
                            return True, 0.5, (x, y, w, h)
            
            return False, 0.0, (0, 0, 0, 0)
        except Exception as e:
            logger.error(f"Error in color-based detection: {e}")
            return False, 0.0, (0, 0, 0, 0)
    
    def shape_based_detection(self, frame: np.ndarray) -> Tuple[bool, float, Tuple[int, int, int, int]]:
        """Detect iPhone using shape analysis."""
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Apply Gaussian blur
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Apply threshold
            _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Find contours
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 2000:  # Minimum area for phone detection
                    x, y, w, h = cv2.boundingRect(contour)
                    aspect_ratio = w / h
                    
                    # Phone-like dimensions
                    if 0.4 <= aspect_ratio <= 0.7 and w > 60 and h > 100:
                        # Check solidity (how "solid" the shape is)
                        hull = cv2.convexHull(contour)
                        hull_area = cv2.contourArea(hull)
                        solidity = area / hull_area if hull_area > 0 else 0
                        
                        if solidity > 0.7:  # Relatively solid shape
                            if self.is_in_detection_area(x, y, w, h):
                                return True, 0.4, (x, y, w, h)
            
            return False, 0.0, (0, 0, 0, 0)
        except Exception as e:
            logger.error(f"Error in shape-based detection: {e}")
            return False, 0.0, (0, 0, 0, 0)
    
    def is_in_detection_area(self, x: int, y: int, w: int, h: int) -> bool:
        """Check if detection is within the specified area."""
        if not self.config['detection_area']['enabled']:
            return True
        
        area = self.config['detection_area']
        return (area['x'] <= x <= area['x'] + area['width'] and
                area['y'] <= y <= area['y'] + area['height'])
    
    def send_notification(self, message: str) -> bool:
        """Send notification using macOS Messages app."""
        # Determine recipient
        recipient = self.config.get('recipient_phone_number') or self.config.get('recipient_email')
        if not recipient:
            logger.warning("No recipient configured. Cannot send notification.")
            return False
        
        # Determine service
        service = self.config.get('message_service', 'iMessage')
        
        # Send with cooldown
        return self.messenger.send_notification_with_cooldown(recipient, message, service)
    
    def draw_detection_info(self, frame: np.ndarray, detected: bool, confidence: float, bbox: Tuple[int, int, int, int]) -> np.ndarray:
        """Draw detection information on the frame."""
        # Draw detection area if enabled
        if self.config['detection_area']['enabled']:
            area = self.config['detection_area']
            cv2.rectangle(frame, (area['x'], area['y']), 
                         (area['x'] + area['width'], area['y'] + area['height']), 
                         (0, 255, 0), 2)
            cv2.putText(frame, "Detection Area", (area['x'], area['y'] - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        
        # Draw detection result
        if detected:
            x, y, w, h = bbox
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, f"iPhone Detected! ({confidence:.2f})", 
                       (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        
        # Draw status info
        status_text = f"Detections: {self.detection_count}"
        cv2.putText(frame, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(frame, timestamp, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        return frame
    
    def run(self):
        """Main detection loop."""
        logger.info("Starting iPhone detection...")
        
        if not self.initialize_camera():
            return
        
        try:
            while True:
                ret, frame = self.camera.read()
                if not ret:
                    logger.error("Failed to read from camera")
                    break
                
                # Detect iPhone
                detected, confidence, bbox = self.detect_iphone(frame)
                
                if detected:
                    self.detection_count += 1
                    current_time = time.time()
                    
                    # Send notification if cooldown period has passed
                    if current_time - self.last_notification_time > self.notification_cooldown:
                        message = f"🚨 iPhone detected! Confidence: {confidence:.2f} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                        
                        if self.send_notification(message):
                            self.last_notification_time = current_time
                            logger.info(f"Notification sent for detection #{self.detection_count}")
                        else:
                            logger.warning("Failed to send notification")
                    else:
                        logger.info(f"iPhone detected (cooldown active) - Detection #{self.detection_count}")
                
                # Draw detection info on frame
                frame = self.draw_detection_info(frame, detected, confidence, bbox)
                
                # Display frame
                cv2.imshow('iPhone Detector', frame)
                
                # Check for exit key
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    logger.info("Exiting...")
                    break
                elif key == ord('s'):
                    # Save current frame
                    filename = f"detection_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                    cv2.imwrite(filename, frame)
                    logger.info(f"Frame saved as {filename}")
        
        except KeyboardInterrupt:
            logger.info("Interrupted by user")
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources."""
        if self.camera:
            self.camera.release()
        cv2.destroyAllWindows()
        logger.info("Cleanup completed")

def main():
    """Main function."""
    print("iPhone Camera Detector with SMS Notifications")
    print("=" * 50)
    print("Controls:")
    print("  'q' - Quit")
    print("  's' - Save current frame")
    print("=" * 50)
    
    detector = iPhoneDetector()
    detector.run()

if __name__ == "__main__":
    main()
