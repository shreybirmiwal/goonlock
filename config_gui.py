#!/usr/bin/env python3
"""
Configuration GUI for iPhone Detector

A simple GUI to configure the detector settings.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from typing import Dict, Any

class ConfigGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("iPhone Detector Configuration")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        self.config_file = "config.json"
        self.config = self.load_config()
        
        self.create_widgets()
        self.load_current_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        default_config = {
            "camera_index": 0,
            "detection_confidence": 0.5,
            "notification_cooldown": 60,
            "recipient_phone_number": "",
            "recipient_email": "",
            "message_service": "iMessage",
            "custom_message": "🚨 Phone detected!",
            "detection_area": {
                "enabled": False,
                "x": 0,
                "y": 0,
                "width": 640,
                "height": 480
            }
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                # Merge with defaults
                for key, value in default_config.items():
                    if key not in config:
                        config[key] = value
                return config
            except Exception as e:
                messagebox.showerror("Error", f"Error loading config: {e}")
                return default_config
        else:
            return default_config
    
    def save_config(self):
        """Save configuration to JSON file."""
        try:
            # Update config with current values
            self.config["camera_index"] = int(self.camera_index_var.get())
            self.config["detection_confidence"] = float(self.confidence_var.get())
            self.config["notification_cooldown"] = int(self.cooldown_var.get())
            self.config["recipient_phone_number"] = self.phone_var.get().strip()
            self.config["recipient_email"] = self.email_var.get().strip()
            self.config["message_service"] = self.service_var.get()
            self.config["custom_message"] = self.message_var.get().strip()
            
            # Save to file
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
            
            messagebox.showinfo("Success", "Configuration saved successfully!")
            
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving config: {e}")
    
    def load_current_config(self):
        """Load current configuration into the GUI fields."""
        self.camera_index_var.set(str(self.config.get("camera_index", 0)))
        self.confidence_var.set(str(self.config.get("detection_confidence", 0.5)))
        self.cooldown_var.set(str(self.config.get("notification_cooldown", 60)))
        self.phone_var.set(self.config.get("recipient_phone_number", ""))
        self.email_var.set(self.config.get("recipient_email", ""))
        self.service_var.set(self.config.get("message_service", "iMessage"))
        self.message_var.set(self.config.get("custom_message", "🚨 Phone detected!"))
    
    def create_widgets(self):
        """Create the GUI widgets."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="iPhone Detector Configuration", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Camera Settings
        camera_frame = ttk.LabelFrame(main_frame, text="Camera Settings", padding="10")
        camera_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(camera_frame, text="Camera Index:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.camera_index_var = tk.StringVar()
        camera_combo = ttk.Combobox(camera_frame, textvariable=self.camera_index_var, 
                                   values=["0", "1", "2", "3"], width=10)
        camera_combo.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        # Detection Settings
        detection_frame = ttk.LabelFrame(main_frame, text="Detection Settings", padding="10")
        detection_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(detection_frame, text="Confidence Threshold:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.confidence_var = tk.StringVar()
        confidence_scale = ttk.Scale(detection_frame, from_=0.1, to=1.0, 
                                    variable=self.confidence_var, orient=tk.HORIZONTAL)
        confidence_scale.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2)
        
        ttk.Label(detection_frame, text="Notification Cooldown (seconds):").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.cooldown_var = tk.StringVar()
        cooldown_entry = ttk.Entry(detection_frame, textvariable=self.cooldown_var, width=10)
        cooldown_entry.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        # Message Settings
        message_frame = ttk.LabelFrame(main_frame, text="Message Settings", padding="10")
        message_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(message_frame, text="Phone Number:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.phone_var = tk.StringVar()
        phone_entry = ttk.Entry(message_frame, textvariable=self.phone_var, width=20)
        phone_entry.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        ttk.Label(message_frame, text="Email (optional):").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.email_var = tk.StringVar()
        email_entry = ttk.Entry(message_frame, textvariable=self.email_var, width=20)
        email_entry.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        ttk.Label(message_frame, text="Service:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.service_var = tk.StringVar()
        service_combo = ttk.Combobox(message_frame, textvariable=self.service_var, 
                                    values=["iMessage", "SMS"], width=10)
        service_combo.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        ttk.Label(message_frame, text="Custom Message:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.message_var = tk.StringVar()
        message_entry = ttk.Entry(message_frame, textvariable=self.message_var, width=30)
        message_entry.grid(row=3, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=(20, 0))
        
        ttk.Button(button_frame, text="Save Configuration", 
                  command=self.save_config).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(button_frame, text="Test Message", 
                  command=self.test_message).grid(row=0, column=1, padx=(0, 10))
        ttk.Button(button_frame, text="Start Detector", 
                  command=self.start_detector).grid(row=0, column=2)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        detection_frame.columnconfigure(1, weight=1)
    
    def test_message(self):
        """Test sending a message with current settings."""
        try:
            from macos_messenger import MacOSMessenger
            
            messenger = MacOSMessenger()
            recipient = self.phone_var.get().strip() or self.email_var.get().strip()
            
            if not recipient:
                messagebox.showerror("Error", "Please enter a phone number or email")
                return
            
            test_message = "🧪 Test message from iPhone Detector Configuration"
            success = messenger.send_message(recipient, test_message, self.service_var.get())
            
            if success:
                messagebox.showinfo("Success", "Test message sent successfully!")
            else:
                messagebox.showerror("Error", "Failed to send test message")
                
        except ImportError:
            messagebox.showerror("Error", "macOS messenger module not found")
        except Exception as e:
            messagebox.showerror("Error", f"Error sending test message: {e}")
    
    def start_detector(self):
        """Start the iPhone detector with current configuration."""
        try:
            import subprocess
            import sys
            
            # Save config first
            self.save_config()
            
            # Start the detector
            subprocess.Popen([sys.executable, "iphone_detector.py"])
            messagebox.showinfo("Success", "iPhone detector started!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error starting detector: {e}")
    
    def run(self):
        """Run the GUI."""
        self.root.mainloop()

def main():
    """Main function."""
    app = ConfigGUI()
    app.run()

if __name__ == "__main__":
    main()
