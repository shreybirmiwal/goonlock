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
from ultralytics import YOLO

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
        
        # Initialize YOLO model
        logger.info("Loading YOLOv8 model...")
        self.model = YOLO("yolov8n.pt")  # nano version for speed
        logger.info("YOLO model loaded successfully")
        
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
        Detect iPhone/phone in the frame using YOLOv8.
        Returns: (detected, confidence, bounding_box)
        """
        try:
            # Run YOLO detection
            results = self.model(frame, verbose=False)
            
            best_confidence = 0.0
            best_bbox = (0, 0, 0, 0)
            detected = False
            
            for r in results:
                for box in r.boxes:
                    cls = int(box.cls[0])
                    label = self.model.names[cls]
                    confidence = float(box.conf[0])
                    
                    # Check if it's a cell phone
                    if label == "cell phone" and confidence > self.config['detection_confidence']:
                        # Get bounding box coordinates
                        x1, y1, x2, y2 = box.xyxy[0].tolist()
                        bbox = (int(x1), int(y1), int(x2 - x1), int(y2 - y1))
                        
                        # Check if it's in the detection area if specified
                        if self.is_in_detection_area(bbox[0], bbox[1], bbox[2], bbox[3]):
                            if confidence > best_confidence:
                                best_confidence = confidence
                                best_bbox = bbox
                                detected = True
            
            return detected, best_confidence, best_bbox
            
        except Exception as e:
            logger.error(f"Error in YOLO detection: {e}")
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
            cv2.putText(frame, f"Phone Detected! ({confidence:.2f})", 
                       (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        
        # Draw status info - always show confidence level
        status_text = f"Detections: {self.detection_count}"
        cv2.putText(frame, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Always show current confidence level
        confidence_text = f"Confidence: {confidence:.2f}"
        confidence_color = (0, 255, 0) if confidence > self.config['detection_confidence'] else (0, 255, 255)
        cv2.putText(frame, confidence_text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, confidence_color, 2)
        
        # Show detection threshold
        threshold_text = f"Threshold: {self.config['detection_confidence']:.2f}"
        cv2.putText(frame, threshold_text, (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Show detection status
        status_color = (0, 0, 255) if detected else (0, 255, 0)
        status_msg = "DETECTED" if detected else "SCANNING"
        cv2.putText(frame, status_msg, (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(frame, timestamp, (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
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
                        message = f"🚨 Phone detected! Confidence: {confidence:.2f} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                        
                        if self.send_notification(message):
                            self.last_notification_time = current_time
                            logger.info(f"Notification sent for detection #{self.detection_count}")
                        else:
                            logger.warning("Failed to send notification")
                    else:
                        logger.info(f"Phone detected (cooldown active) - Detection #{self.detection_count}")
                
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
    print("Phone Camera Detector with macOS Messages")
    print("=" * 50)
    print("Using YOLOv8 for accurate phone detection")
    print("Controls:")
    print("  'q' - Quit")
    print("  's' - Save current frame")
    print("=" * 50)
    
    detector = iPhoneDetector()
    detector.run()

if __name__ == "__main__":
    main()
