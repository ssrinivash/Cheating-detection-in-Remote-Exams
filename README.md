# Cheating-detection-in-Remote-Exams
Malpractice Detection System
Overview
This application is an AI-powered proctoring system designed to detect potential cheating behaviors during exams or assessments. Using computer vision and audio monitoring, it can identify suspicious activities such as looking away from the screen, speaking, having multiple people present, or not being fully visible on camera.

Features
Face Detection and Tracking: Monitors the presence and position of the user's face
Eye Movement Detection: Detects when the user is looking left, right, up, or down
Multiple Person Detection: Alerts when more than one person is detected in frame
Speech Detection: Uses microphone input to detect if the user is speaking
Automatic Logging: Records all violations with timestamps in a log file
Screenshot Capture: Takes and saves screenshots when violations are detected
Real-time Visual Alerts: Displays warnings directly on the video feed
Requirements
Python 3.6+
OpenCV (cv2)
MediaPipe
NumPy
SoundDevice
Webcam
Microphone
Installation
Install the required dependencies:
pip install opencv-python mediapipe numpy sounddevice
Clone or download this repository to your local machine.
Configuration
Before running the application, you may want to customize these settings in the code:

Screenshot Path: The system currently saves screenshots to C:\Users\Lenovo\Pictures\Screenshots\cheat. Update this path in the code to match your preferred location.
Alert Sensitivity: You can adjust detection thresholds in the main loop for eye movement, mouth opening, etc.
Camera Input: The system uses the default camera (index 0). If you have multiple cameras, you may need to change this.
Usage
Run the script:
python malpractice_detection.py
Position yourself appropriately in front of the camera.
The system will monitor for the following behaviors:
Looking left or right
Looking up or down
Having your mouth open (possibly talking)
Moving your face too far from the camera
Having another person visible
Speaking (detected via microphone)
Violations will:
Trigger a visual alert on screen
Be logged to violation_log.txt
Result in a screenshot saved to the configured folder
Press 'Q' to exit the application.
How It Works
Face Mesh: Uses MediaPipe's face mesh to track 468 facial landmarks
Eye Tracking: Calculates the relative position of the iris within the eye
Audio Monitoring: Continuously samples microphone volume to detect speech
Threading: Uses a separate thread for audio processing to maintain performance
Security and Privacy Considerations
All data is processed locally on your machine
Screenshots are saved locally and not transmitted
Consider the privacy implications before using this in shared environments
Troubleshooting
If face detection is unreliable, ensure you have adequate lighting
Webcam must be properly connected and accessible
Check microphone permissions if voice detection isn't working
Acknowledgements
This system utilizes Google's MediaPipe library for facial landmark detection.

