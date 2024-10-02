# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 19:47:39 2024

@author: danie
"""

import tkinter as tk
import os
import time
import threading
from playsound import playsound
from PIL import Image, ImageTk
import random
import string
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Constants
DROPLET_IMAGES = [
    resource_path(r'images\drop1.png'),  # Replace with your droplet images
    resource_path(r'images\drop2.png'),
    resource_path(r'images\drop3.png')
]
BLUSH_IMAGE_PATH = resource_path(r'images\blush.png')  # Replace with your blush image path
WIN_SOUND_FILE = resource_path(r'audio\end.mp3')  # Replace with your winning sound file

class WetWindow:
    def __init__(self, master):
        self.master = master
        self.master.config(bg="pink")  # Set the entire window background to pink

        self.label = tk.Label(master, text="I am captcha. Insert USB if human.", padx=20, pady=20, bg="pink")
        self.label.pack()
        self.canvas = tk.Canvas(master, width=500, height=200, bg="pink", highlightthickness=0)
        self.canvas.pack()

        # Load the blush image
        self.blush_image = ImageTk.PhotoImage(Image.open(BLUSH_IMAGE_PATH).resize((100, 50)))  # Resize as needed
        self.blush = None  # To keep track of the blush effect

        # List to keep track of droplet images
        self.droplets = []
        self.max_attempts = 6  # Maximum attempts needed to win
        self.droplet_count = 3  # Number of droplets to show

    def update_text(self, new_text):
        self.label.config(text=new_text)

    def add_droplet(self, attempt):
        # Only show a droplet for the attempts we want
        if attempt >= self.droplet_count:
            return

        # Select a random droplet image
        droplet_image_path = random.choice(DROPLET_IMAGES)
        droplet_image = Image.open(droplet_image_path).convert("RGBA")
        droplet_image = droplet_image.resize((60, 60))  # Make droplet larger

        # Position droplet at the edges of the window
        edge_position = random.choice([
            (0, random.randint(0, 140)),   # Left edge
            (240, random.randint(0, 140)),  # Right edge
            (random.randint(0, 270), 0),    # Top edge
            (random.randint(0, 270), 140)   # Bottom edge
        ])
        x, y = edge_position

        # Add droplet to the canvas
        droplet_tk = ImageTk.PhotoImage(droplet_image)
        self.canvas.create_image(x, y, anchor=tk.NW, image=droplet_tk)

        # Keep a reference to prevent garbage collection
        self.canvas.image = droplet_tk
        self.droplets.append(droplet_tk)  # Keep track of droplets that have been added

    def apply_blush_effect(self):
        # Position the blush image on the canvas
        if self.blush is None:
            self.blush = self.canvas.create_image(150, 90, anchor=tk.CENTER, image=self.blush_image)  # Positioned under the text

    def shake_window(self):
        # Function to vibrate the window when the player wins
        for _ in range(10):  # Number of shake iterations
            self.master.geometry(f"{self.master.winfo_width()}x{self.master.winfo_height()}+{random.randint(-5, 5)}+{random.randint(-5, 5)}")
            self.master.update()
            time.sleep(0.05)  # Duration of each shake

def check_usb(wet_window, sound_file):
    usb_attempts = 0
    first_insertion = True  # Flag to track the first insertion
    start_time = time.time()
    win_interval = 20  # Time window for attempts in seconds
    start_interval = time.time()  # Start time for the first 15 seconds
    usb_inserted = False  # Track if the USB is currently inserted

    while True:
        drives = string.ascii_uppercase  # All possible drive letters
        usb_detected = False

        for drive in drives:
            drive_path = f"{drive}:\\"  # Check each drive letter
            if os.path.exists(drive_path) and os.path.isdir(drive_path):
                # Check if the drive is a removable USB drive
                if "Removable" in os.popen(f"wmic logicaldisk get description | findstr {drive}").read():
                    usb_detected = True
                    break

        if usb_detected and not usb_inserted:
            # USB was just inserted
            usb_inserted = True
            if first_insertion:
                play_sound(sound_file)  # Play sound only on first insertion
                wet_window.apply_blush_effect()  # Apply blush effect on first insertion
                first_insertion = False  # Set flag to False after the first insertion
                wet_window.update_text("Do it again!")
            else:
                usb_attempts += 1
                wet_window.add_droplet(usb_attempts)  # Add droplet effect based on the attempt

            wet_window.update_text(f"Attempt {usb_attempts + 1}/{wet_window.max_attempts}. More!")

            
            if usb_attempts == wet_window.max_attempts-2:
                 wet_window.update_text(f"Attempt {usb_attempts + 1}/{wet_window.max_attempts}. Don't stop! I'm so close!")
            # Check if we've reached the maximum attempts
            if usb_attempts == wet_window.max_attempts-1:
                play_sound(WIN_SOUND_FILE)  # Play win sound when player wins
                wet_window.update_text("You did it! You are true human.")
                wet_window.shake_window()  # Shake the window upon winning
                break

        elif not usb_detected and usb_inserted:
            # USB was just removed
            usb_inserted = False  # Reset the flag since the USB is no longer inserted

        if time.time() - start_interval >= win_interval:
            wet_window.update_text("Only robots don't care about others' pleasure! You are not human.")
            break

        time.sleep(0.1)  # Short sleep before next check

def play_sound(sound_file):
    # Load and play the audio file using playsound
    playsound(sound_file)

def main(sound_file):
    root = tk.Tk()
    root.title("Freaky Captcha Window")
    root.geometry("500x200")  # Set window size

    wet_window = WetWindow(root)

    # Start a thread to check for USB insertion
    threading.Thread(target=check_usb, args=(wet_window, sound_file), daemon=True).start()

    # Start the application
    root.mainloop()

if __name__ == "__main__":
    # Specify the path to your custom sound file here
    sound_file = resource_path(r'audio\insert_usb.wav')  # Replace with the actual path to your sound file
    main(sound_file)
