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
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
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
            "recipients": [
                {
                    "name": "Mom",
                    "phone": "",
                    "message": "I'm on my phone while working!"
                }
            ],
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
            
            # Get recipients from the list
            recipients = []
            for i in range(self.recipients_listbox.size()):
                item = self.recipients_listbox.get(i)
                # Parse the display format: "Name - Phone - Message"
                parts = item.split(" - ", 2)
                if len(parts) == 3:
                    recipients.append({
                        "name": parts[0],
                        "phone": parts[1],
                        "message": parts[2]
                    })
            
            self.config["recipients"] = recipients
            
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
        
        # Load recipients
        recipients = self.config.get("recipients", [])
        for recipient in recipients:
            display_text = f"{recipient['name']} - {recipient['phone']} - {recipient['message']}"
            self.recipients_listbox.insert(tk.END, display_text)
        
        # Update status after loading
        self.update_status()
    
    def create_widgets(self):
        """Create the GUI widgets."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="iPhone Detector Configuration", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Status indicator
        self.status_label = ttk.Label(main_frame, text="📋 Step 1: Configure your settings below", 
                                     font=("Arial", 10), foreground="blue")
        self.status_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Camera Settings
        camera_frame = ttk.LabelFrame(main_frame, text="Camera Settings", padding="10")
        camera_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(camera_frame, text="Camera Index:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.camera_index_var = tk.StringVar()
        camera_combo = ttk.Combobox(camera_frame, textvariable=self.camera_index_var, 
                                   values=["0", "1", "2", "3"], width=10)
        camera_combo.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        # Detection Settings
        detection_frame = ttk.LabelFrame(main_frame, text="Detection Settings", padding="10")
        detection_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(detection_frame, text="Confidence Threshold:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.confidence_var = tk.StringVar()
        confidence_scale = ttk.Scale(detection_frame, from_=0.1, to=1.0, 
                                    variable=self.confidence_var, orient=tk.HORIZONTAL)
        confidence_scale.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2)
        
        ttk.Label(detection_frame, text="Notification Cooldown (seconds):").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.cooldown_var = tk.StringVar()
        cooldown_entry = ttk.Entry(detection_frame, textvariable=self.cooldown_var, width=10)
        cooldown_entry.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        # Recipients Settings
        recipients_frame = ttk.LabelFrame(main_frame, text="Recipients", padding="10")
        recipients_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Recipients list
        ttk.Label(recipients_frame, text="Recipients:").grid(row=0, column=0, sticky=tk.W, pady=2)
        
        # Listbox with scrollbar
        listbox_frame = ttk.Frame(recipients_frame)
        listbox_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=2)
        
        self.recipients_listbox = tk.Listbox(listbox_frame, height=10, width=80)
        scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.recipients_listbox.yview)
        self.recipients_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.recipients_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Recipient input fields
        input_frame = ttk.Frame(recipients_frame)
        input_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Label(input_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(input_frame, textvariable=self.name_var, width=20)
        name_entry.grid(row=0, column=1, padx=(0, 10))
        
        ttk.Label(input_frame, text="Phone:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.phone_var = tk.StringVar()
        phone_entry = ttk.Entry(input_frame, textvariable=self.phone_var, width=20)
        phone_entry.grid(row=0, column=3, padx=(0, 10))
        
        ttk.Label(input_frame, text="Message:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        self.message_var = tk.StringVar()
        message_entry = ttk.Entry(input_frame, textvariable=self.message_var, width=60)
        message_entry.grid(row=1, column=1, columnspan=3, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # Recipient buttons
        recipient_buttons = ttk.Frame(recipients_frame)
        recipient_buttons.grid(row=3, column=0, columnspan=3, pady=(10, 0))
        
        ttk.Button(recipient_buttons, text="Add Recipient", 
                  command=self.add_recipient).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(recipient_buttons, text="Remove Selected", 
                  command=self.remove_recipient).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(recipient_buttons, text="Test All Messages", 
                  command=self.test_all_messages).grid(row=0, column=2)
        
        # Main buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=(20, 0))
        
        ttk.Button(button_frame, text="Save Configuration", 
                  command=self.save_config).grid(row=0, column=0, padx=(0, 10))
        
        # Make Start Detector button more prominent
        start_button = ttk.Button(button_frame, text="🚀 START DETECTOR", 
                                 command=self.start_detector)
        start_button.grid(row=0, column=1, padx=(0, 10))
        
        # Add help button
        ttk.Button(button_frame, text="❓ Help", 
                  command=self.show_help).grid(row=0, column=2)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        detection_frame.columnconfigure(1, weight=1)
        listbox_frame.columnconfigure(0, weight=1)
        listbox_frame.rowconfigure(0, weight=1)
        input_frame.columnconfigure(3, weight=1)
    
    def add_recipient(self):
        """Add a new recipient to the list."""
        name = self.name_var.get().strip()
        phone = self.phone_var.get().strip()
        message = self.message_var.get().strip()
        
        if not name or not phone or not message:
            messagebox.showerror("Error", "Please fill in all fields (Name, Phone, Message)")
            return
        
        display_text = f"{name} - {phone} - {message}"
        self.recipients_listbox.insert(tk.END, display_text)
        
        # Clear input fields
        self.name_var.set("")
        self.phone_var.set("")
        self.message_var.set("")
        
        # Update status
        self.update_status()
    
    def remove_recipient(self):
        """Remove selected recipient from the list."""
        selection = self.recipients_listbox.curselection()
        if selection:
            self.recipients_listbox.delete(selection[0])
            self.update_status()
        else:
            messagebox.showwarning("Warning", "Please select a recipient to remove")
    
    def test_all_messages(self):
        """Test sending messages to all recipients."""
        try:
            from macos_messenger import MacOSMessenger
            
            if self.recipients_listbox.size() == 0:
                messagebox.showerror("Error", "No recipients configured")
                return
            
            messenger = MacOSMessenger()
            success_count = 0
            
            for i in range(self.recipients_listbox.size()):
                item = self.recipients_listbox.get(i)
                parts = item.split(" - ", 2)
                if len(parts) == 3:
                    name, phone, message = parts
                    test_message = f"🧪 Test from {name}: {message}"
                    
                    if messenger.send_message(phone, test_message, "iMessage"):
                        success_count += 1
            
            if success_count > 0:
                messagebox.showinfo("Success", f"Test messages sent to {success_count} recipients!")
            else:
                messagebox.showerror("Error", "Failed to send test messages")
                
        except ImportError:
            messagebox.showerror("Error", "macOS messenger module not found")
        except Exception as e:
            messagebox.showerror("Error", f"Error sending test messages: {e}")
    
    def start_detector(self):
        """Start the iPhone detector with current configuration."""
        try:
            import subprocess
            import sys
            
            # Check if recipients are configured
            if self.recipients_listbox.size() == 0:
                messagebox.showerror("Error", "Please add at least one recipient before starting the detector!")
                return
            
            # Save config first
            self.save_config()
            
            # Start the detector
            subprocess.Popen([sys.executable, "iphone_detector.py"])
            messagebox.showinfo("Success", 
                              "🚀 iPhone detector started!\n\n"
                              "The camera window should open shortly.\n"
                              "Press 'q' in the camera window to quit.\n"
                              "Press 's' to save a frame.\n\n"
                              "The detector will randomly send messages to your configured recipients when phones are detected!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error starting detector: {e}")
    
    def show_help(self):
        """Show help information."""
        help_text = """
📱 iPhone Detector Help

1. CONFIGURE RECIPIENTS:
   • Add people with their phone numbers and custom messages
   • Example: "Mom" - "5129427299" - "I'm on my phone while working!"

2. TEST YOUR SETUP:
   • Click "Test All Messages" to verify messaging works
   • Make sure Messages app permissions are granted

3. START DETECTION:
   • Click "🚀 START DETECTOR" to begin monitoring
   • A camera window will open showing the live feed
   • The detector will randomly pick someone to text when a phone is detected

4. CONTROLS:
   • Press 'q' in camera window to quit
   • Press 's' in camera window to save current frame

5. PERMISSIONS:
   • Go to System Preferences > Security & Privacy > Privacy > Automation
   • Allow Terminal/IDE to control Messages app

6. TROUBLESHOOTING:
   • Make sure you've sent at least one message manually to each recipient first
   • Check that phone numbers are in correct format (+1XXXXXXXXXX)
   • Verify Messages app is signed in to your Apple ID
        """
        
        # Create help window
        help_window = tk.Toplevel(self.root)
        help_window.title("Help - iPhone Detector")
        help_window.geometry("600x500")
        help_window.resizable(False, False)
        
        # Create text widget with scrollbar
        text_frame = ttk.Frame(help_window, padding="10")
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        text_widget = tk.Text(text_frame, wrap=tk.WORD, font=("Arial", 10))
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_widget.insert(tk.END, help_text)
        text_widget.config(state=tk.DISABLED)
        
        # Close button
        ttk.Button(help_window, text="Close", command=help_window.destroy).pack(pady=10)
    
    def update_status(self):
        """Update the status label based on current configuration."""
        recipient_count = self.recipients_listbox.size()
        
        if recipient_count == 0:
            self.status_label.config(text="📋 Step 1: Add at least one recipient to continue", 
                                   foreground="red")
        elif recipient_count == 1:
            self.status_label.config(text="✅ Ready! Click '🚀 START DETECTOR' to begin monitoring", 
                                   foreground="green")
        else:
            self.status_label.config(text=f"✅ Ready! {recipient_count} recipients configured. Click '🚀 START DETECTOR' to begin", 
                                   foreground="green")
    
    def run(self):
        """Run the GUI."""
        self.root.mainloop()

def main():
    """Main function."""
    app = ConfigGUI()
    app.run()

if __name__ == "__main__":
    main()
