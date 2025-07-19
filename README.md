# Eye-Controlled Mouse with Blink Clicks

This project enables hands-free mouse control using your eyes and blinks, powered by MediaPipe Face Mesh, OpenCV, and PyAutoGUI. The mouse cursor follows your gaze, and you can perform left and right clicks by double or triple blinking, respectively.

## Features
- Move the mouse cursor by looking at different parts of the screen
- Double blink to left click
- Triple blink to right click
- Real-time webcam-based tracking
- Uses only a standard webcam and Python libraries

## How It Works
- Uses MediaPipe Face Mesh to detect facial landmarks
- Estimates gaze direction from both eyes to move the cursor
- Detects blinks using the Eye Aspect Ratio (EAR)
- Counts blinks within a short time window to distinguish double and triple blinks

## Requirements
- Python 3.8+
- OpenCV (`opencv-python`)
- MediaPipe
- PyAutoGUI
- NumPy

Install all dependencies with:
```bash
pip install -r requirements.txt
```

## Usage
1. Connect a webcam to your computer.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the script:
   ```bash
   python eye_control.py
   ```
4. Look at different parts of the screen to move the cursor.
5. Double blink to left click, triple blink to right click.
6. Press `q` to quit.

## File Structure
```
├── eye_control.py        # Main script for eye-controlled mouse
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```
