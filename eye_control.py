import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True)

# Get screen width and height
screen_width, screen_height = pyautogui.size()

# Eye landmark indices for left and right eyes (outer, inner, top, bottom)
LEFT_EYE = [33, 133, 159, 145]   # [outer, inner, top, bottom]
RIGHT_EYE = [362, 263, 386, 374] # [outer, inner, top, bottom]

# Eye aspect ratio calculation

def eye_aspect_ratio(eye_landmarks):
    # eye_landmarks: [outer, inner, top, bottom]
    # EAR = (||top-bottom||) / (||outer-inner||)
    top = np.array([eye_landmarks[2].x, eye_landmarks[2].y])
    bottom = np.array([eye_landmarks[3].x, eye_landmarks[3].y])
    outer = np.array([eye_landmarks[0].x, eye_landmarks[0].y])
    inner = np.array([eye_landmarks[1].x, eye_landmarks[1].y])
    vert = np.linalg.norm(top - bottom)
    horiz = np.linalg.norm(outer - inner)
    return vert / horiz if horiz != 0 else 0

# Blink detection parameters
EAR_THRESH = 0.20
BLINK_MIN_FRAMES = 2
BLINK_MAX_INTERVAL = 0.5  # seconds between blinks for multi-blink

# Blink state
blink_count = 0
last_blink_time = 0
blink_timestamps = []

# Start webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmarks = output.multi_face_landmarks
    frame_height, frame_width, _ = frame.shape

    if landmarks:
        face_landmark = landmarks[0]
        lm = face_landmark.landmark
        # Get left and right eye landmarks
        left_eye_pts = [lm[i] for i in LEFT_EYE]
        right_eye_pts = [lm[i] for i in RIGHT_EYE]

        # Calculate EAR for both eyes
        left_ear = eye_aspect_ratio(left_eye_pts)
        right_ear = eye_aspect_ratio(right_eye_pts)
        avg_ear = (left_ear + right_ear) / 2

        # Blink detection
        if avg_ear < EAR_THRESH:
            if last_blink_time == 0 or (time.time() - last_blink_time) > 0.2:
                blink_timestamps.append(time.time())
                last_blink_time = time.time()
        else:
            last_blink_time = 0

        # Remove old blinks
        blink_timestamps = [t for t in blink_timestamps if time.time() - t < 2]
        # Count blinks in last 1 second
        recent_blinks = [t for t in blink_timestamps if time.time() - t < 1]
        if len(recent_blinks) == 2:
            pyautogui.click(button='left')
            blink_timestamps = []
        elif len(recent_blinks) == 3:
            pyautogui.click(button='right')
            blink_timestamps = []

        # Gaze estimation: use the center between both eyes
        left_eye_center = np.array([
            (left_eye_pts[0].x + left_eye_pts[1].x) / 2,
            (left_eye_pts[2].y + left_eye_pts[3].y) / 2
        ])
        right_eye_center = np.array([
            (right_eye_pts[0].x + right_eye_pts[1].x) / 2,
            (right_eye_pts[2].y + right_eye_pts[3].y) / 2
        ])
        eye_center = (left_eye_center + right_eye_center) / 2
        x = int(eye_center[0] * frame_width)
        y = int(eye_center[1] * frame_height)
        # Map to screen
        screen_x = np.interp(x, [0, frame_width], [0, screen_width])
        screen_y = np.interp(y, [0, frame_height], [0, screen_height])
        pyautogui.moveTo(screen_x, screen_y)

        # Draw eyes and center
        for pt in left_eye_pts + right_eye_pts:
            cx, cy = int(pt.x * frame_width), int(pt.y * frame_height)
            cv2.circle(frame, (cx, cy), 2, (0, 255, 0), -1)
        cv2.circle(frame, (x, y), 5, (255, 0, 255), -1)

    cv2.imshow("Eye Controlled Mouse", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows() 