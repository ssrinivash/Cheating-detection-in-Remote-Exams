#malpractice detection system 
import cv2
import mediapipe as mp
import numpy as np
import sounddevice as sd
import datetime
import threading
import os

# ================== MIC SETUP ==================
mic_volume = 0
def audio_listener():
    global mic_volume
    def callback(indata, frames, time, status):
        mic_volume = np.linalg.norm(indata) * 10
    with sd.InputStream(callback=callback):
        sd.sleep(1000000)
threading.Thread(target=audio_listener, daemon=True).start()

# ================== MEDIAPIPE ==================
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True, max_num_faces=2)
drawing_spec = mp.solutions.drawing_utils.DrawingSpec(thickness=1, circle_radius=1)

cap = cv2.VideoCapture(0)

# ================== LOGGING & SCREENSHOT ==================
# Custom path for screenshots
screenshot_folder = r"C:\Users\Lenovo\Pictures\Screenshots"
cheat_folder = os.path.join(screenshot_folder, "cheat")

# Ensure the 'cheat' folder exists inside the custom screenshot path
if not os.path.exists(cheat_folder):
    os.makedirs(cheat_folder)

def log_violation(message):
    # Logging with utf-8 encoding to handle special characters
    with open("violation_log.txt", "a", encoding="utf-8") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {message}\n")

def capture_screenshot(frame, alert_text):
    # Generate timestamp for the screenshot filename
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_filename = os.path.join(cheat_folder, f"screenshot_{timestamp}.png")
    
    # Save the screenshot in the 'cheat' folder
    cv2.imwrite(screenshot_filename, frame)
    print(f"Screenshot saved as {screenshot_filename}")

def draw_alert(frame, text, color=(0, 0, 255)):
    font = cv2.FONT_HERSHEY_COMPLEX
    cv2.putText(frame, text, (20, 40), font, 0.8, color, 2, cv2.LINE_AA)

# ================== MAIN LOOP ==================
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (960, 720))
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    alert_text = ""

    if results.multi_face_landmarks:
        face_count = len(results.multi_face_landmarks)

        # 🔸 If more than 1 face: second person detected
        if face_count > 1:
            alert_text = "⚠️ Second Person Detected!"
        else:
            landmarks = results.multi_face_landmarks[0].landmark

            left_eye_inner = landmarks[133]
            left_eye_outer = landmarks[33]
            left_iris = landmarks[468]

            right_eye_inner = landmarks[362]
            right_eye_outer = landmarks[263]
            right_iris = landmarks[473]

            top_lip = landmarks[13]
            bottom_lip = landmarks[14]
            chin = landmarks[152]
            forehead = landmarks[10]

            l_w = abs(left_eye_outer.x - left_eye_inner.x)
            r_w = abs(right_eye_outer.x - right_eye_inner.x)
            l_rel = (left_iris.x - left_eye_outer.x) / l_w
            r_rel = (right_iris.x - right_eye_inner.x) / r_w

            if l_rel < 0.25 and r_rel < 0.25:
                alert_text = "⚠️ Looking left"
            elif l_rel > 0.75 and r_rel > 0.75:
                alert_text = "⚠️ Looking right"
            elif abs(left_iris.y - left_eye_inner.y) > 0.02:
                alert_text = "⚠️ Looking up/down"

            mouth_gap = abs(top_lip.y - bottom_lip.y) * h
            if mouth_gap > 18:
                alert_text = "⚠️ Mouth open"

            face_height = abs(chin.y - forehead.y) * h
            if face_height < h * 0.3:
                alert_text = "⚠️ Face not fully visible"

            mp.solutions.drawing_utils.draw_landmarks(
                frame, results.multi_face_landmarks[0],
                mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=drawing_spec
            )
    else:
        alert_text = "⚠️ Face not detected!"

    # 🎤 Mic voice detection
    if mic_volume > 2.0:
        alert_text = "⚠️ Speaking (Mic)"

    if alert_text:
        draw_alert(frame, alert_text)
        log_violation(alert_text)
        capture_screenshot(frame, alert_text)  # Take screenshot when alert is shown
    else:
        draw_alert(frame, "✅ Face OK", color=(0, 255, 0))

    cv2.imshow("Cheating Detection Proctor (Press Q to Quit)", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
