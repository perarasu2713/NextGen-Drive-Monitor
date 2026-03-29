import cv2
import mediapipe as mp
import numpy as np
from scipy.spatial import distance as dist
import pygame
from collections import deque
import csv
import time
import warnings
warnings.filterwarnings("ignore")

# -------------------- SOUND --------------------
pygame.mixer.init()
pygame.mixer.music.load("fire-alarm.mp3")
pygame.mixer.music.set_volume(1.0)

# 🔥 SINGLE SOURCE OF TRUTH
SOUND_ON = True

def start_alarm():
    if SOUND_ON:
        # 🔥 prevent multiple overlapping sounds
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)

def stop_alarm():
    pygame.mixer.music.stop()

# -------------------- MEDIAPIPE --------------------
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]
MOUTH = [13, 14, 78, 308]

# -------------------- FUNCTIONS --------------------
def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

def mouth_aspect_ratio(mouth):
    A = dist.euclidean(mouth[0], mouth[1])
    C = dist.euclidean(mouth[2], mouth[3])
    return A / C

# -------------------- CSV --------------------
csv_file = open("session_data.csv", mode="w", newline="")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Time", "EAR", "MAR", "Blinks", "Yawns", "Drowsy"])

# -------------------- THRESHOLDS --------------------
EAR_THRESHOLD = 0.18
MAR_THRESHOLD = 0.4
YAWN_FRAME_THRESHOLD = 10

# -------------------- VARIABLES --------------------
COUNTER = 0
ALARM_ON = False

TOTAL_BLINKS = 0
EYE_CLOSED = False

YAWN_COUNTER = 0
TOTAL_YAWNS = 0

ear_history = deque(maxlen=100)

# -------------------- MAIN FUNCTION --------------------
def process_frame(frame):
    global COUNTER, ALARM_ON, TOTAL_BLINKS, EYE_CLOSED
    global YAWN_COUNTER, TOTAL_YAWNS

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:

        cv2.putText(frame, "FACE DETECTED", (30, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

        for face_landmarks in results.multi_face_landmarks:

            h, w, _ = frame.shape
            left_eye, right_eye, mouth = [], [], []

            for idx in LEFT_EYE:
                x = int(face_landmarks.landmark[idx].x * w)
                y = int(face_landmarks.landmark[idx].y * h)
                left_eye.append((x, y))

            for idx in RIGHT_EYE:
                x = int(face_landmarks.landmark[idx].x * w)
                y = int(face_landmarks.landmark[idx].y * h)
                right_eye.append((x, y))

            for idx in MOUTH:
                x = int(face_landmarks.landmark[idx].x * w)
                y = int(face_landmarks.landmark[idx].y * h)
                mouth.append((x, y))

            ear = (eye_aspect_ratio(left_eye) +
                   eye_aspect_ratio(right_eye)) / 2.0
            mar = mouth_aspect_ratio(mouth)

            # DISPLAY
            cv2.putText(frame, f"EAR: {ear:.2f}", (30, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

            cv2.putText(frame, f"Blinks: {TOTAL_BLINKS}", (30, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

            cv2.putText(frame, f"MAR: {mar:.2f}", (30, 120),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)

            cv2.putText(frame, f"Yawns: {TOTAL_YAWNS}", (30, 150),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 255), 2)

            # -------------------- BLINK --------------------
            if ear < EAR_THRESHOLD:
                if not EYE_CLOSED:
                    EYE_CLOSED = True
            else:
                if EYE_CLOSED:
                    TOTAL_BLINKS += 1
                EYE_CLOSED = False

            # -------------------- DROWSINESS --------------------
            if ear < EAR_THRESHOLD:
                COUNTER += 1
            else:
                COUNTER = 0

            if COUNTER >= 20:
                cv2.putText(frame, "DROWSINESS ALERT!", (50, 200),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

                # 🔥 FIXED LOGIC
                if SOUND_ON:
                    start_alarm()

                ALARM_ON = True

            else:
                if ALARM_ON:
                    stop_alarm()
                    ALARM_ON = False

            # -------------------- YAWN --------------------
            if mar > MAR_THRESHOLD:
                YAWN_COUNTER += 1
            else:
                if YAWN_COUNTER >= YAWN_FRAME_THRESHOLD:
                    TOTAL_YAWNS += 1
                YAWN_COUNTER = 0

            # -------------------- CSV --------------------
            current_time = round(time.time(), 2)
            drowsy_status = 1 if COUNTER >= 20 else 0

            csv_writer.writerow([
                current_time,
                round(ear, 3),
                round(mar, 3),
                TOTAL_BLINKS,
                TOTAL_YAWNS,
                drowsy_status
            ])

    else:
        cv2.putText(frame, "NO FACE DETECTED", (30, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    return frame