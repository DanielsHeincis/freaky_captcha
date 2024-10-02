# USB Captcha Application

This application serves as a fun CAPTCHA system that interacts with USB insertion. When a USB drive is detected, the window changes and prompts the user to continue.
To download Windows executable use this Mega link (it was too big for Github) - [mega.nz](https://mega.nz/file/8VcmGZwK#rBezIb_SQ8mrsV_1bpUqAe60WhGj0JNyrlEn66JEjFA). 
If that doesn't work then folow instruction down here and run it from terminal as Python file.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [License](#license)

## Prerequisites

Before you begin, ensure you have met the following requirements:

- **Python**: You need Python 3.6 or later installed on your machine. Download it from [python.org](https://www.python.org/downloads/).
- **Pip**: Ensure `pip` is installed (it comes with Python installations by default).

## Installation

1. **Download the Project**:
   - Extract the contents of the provided ZIP file to a directory of your choice.

2. **Open a Terminal/Command Prompt**:
   - Navigate to the directory where you extracted the project files.

3. **Install Required Libraries**:
   - Run the following command to install the necessary libraries:
     ```bash
     pip install -r requirements.txt
     ```

## Running the Application

1. **Place Your Audio and Image Files**:
   - Ensure you have the required audio files (`insert_usb.wav` and `end.mp3`) and droplet images in the `audio` and `images` folders respectively. The project should include these folders.

2. **Run the Application**:
   - In the terminal or command prompt, execute the following command:
     ```bash
     python captcha_app.py
     ```
   - This will launch the application window.

3. **Interact with the Application**:
   - Follow the prompts in the GUI. Insert a USB device to see the interaction and complete the CAPTCHA.

