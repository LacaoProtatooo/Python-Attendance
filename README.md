# Face Recognition Attendance System

A Python-based attendance system with Tkinter GUI using OpenCV face recognition with real-time visual feedback.

## Features

- ✅ Modern Tkinter GUI interface
- ✅ Real-time face detection with visual indicators (green box when detected, red warning when not)
- ✅ Progress bar showing sample collection status during registration
- ✅ Flash effect when capturing samples
- ✅ Non-blocking capture (only captures when face is detected)
- ✅ Automatic attendance marking with CSV export
- ✅ Clear status messages and user feedback

## Installation

### Required Packages

```bash
pip install opencv-python opencv-contrib-python numpy pillow
```

## Usage

1. Run the program:
```bash
python main.py
```

2. The GUI will open with two main sections:
   - **Left side**: Camera feed with real-time detection
   - **Right side**: Controls for registration and attendance

### Registering New Faces

1. Enter the person's name in the text field
2. Click "Start Registration"
3. Look at the camera
4. Wait for the green rectangle (face detected indicator)
5. 30 samples will be automatically captured with visual feedback
6. Progress bar shows collection status in real-time
7. Status text shows "CAPTURING..." when face detected or "WAITING FOR FACE..." when not
8. Model automatically trains after registration

### Taking Attendance

1. Click "Start Attendance"
2. Face the camera
3. Attendance is automatically marked when recognized
4. Green box shows recognized faces, red for unknown
5. Results are saved to `Attendance_YYYY-MM-DD.csv`

## Visual Indicators

- **Green Rectangle**: Face detected, capturing samples
- **Red Text**: No face detected, please position your face
- **White Flash**: Sample captured successfully
- **Progress Bar**: Shows collection progress (updates in real-time)
- **Status Text**: Real-time feedback on system state

## GUI Features

- Modern dark theme interface
- Real-time camera feed display (640x480)
- Progress tracking during registration
- Separate controls for registration and attendance
- Stop camera button
- Re-train model button
- Instructions panel
- Status indicators

## Project Structure

```
Face_recognition_based_attendance_system/
├── main.py                          # Main application with Tkinter GUI
├── images/                          # Stored face samples
├── face_recognizer.yml              # Trained face recognition model
├── labels.pkl                       # Label mappings
├── Attendance_YYYY-MM-DD.csv       # Daily attendance records
└── README.md                        # This file
```

## Requirements

- Python 3.7+
- Webcam
- opencv-python
- opencv-contrib-python
- numpy
- pillow (for Tkinter image display)

## Controls

- **Start Registration**: Begin face registration process
- **Start Attendance**: Begin attendance marking
- **Stop Camera**: Stop the camera feed
- **Re-train Model**: Rebuild face recognition model from existing images

## Troubleshooting

**Camera not opening:**
- Check if another application is using the camera
- Verify camera permissions

**Slow performance:**
- Close other applications using the camera
- Ensure good lighting conditions

**Face not detected:**
- Ensure good lighting
- Position your face directly in front of the camera
- Remove glasses if they cause issues
- Keep your face within the camera frame

**GUI not displaying properly:**
- Ensure Pillow is installed: `pip install pillow`
- Check screen resolution compatibility

## Notes

- The system uses OpenCV's LBPH face recognizer
- Attendance is saved in CSV format with Name, Date, and Time
- Each person can only mark attendance once per day
- The camera feed is displayed at 640x480 resolution
- Registration requires 30 face samples for better accuracy

## License

This project is open-source and available under the MIT License.
