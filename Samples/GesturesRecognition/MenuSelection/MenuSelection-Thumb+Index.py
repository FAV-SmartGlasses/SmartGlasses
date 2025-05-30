import cv2
import mediapipe as mp
import math
from collections import deque

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

cap = cv2.VideoCapture(0)

DIST_THRESHOLD = 40
GESTURE_SEQUENCE = ['open', 'closed', 'open', 'closed']
state_history = deque(maxlen=20)
gesture_detected = False

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    h, w, _ = image.shape
    gesture_detected = False

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            def get_point(identifier):
                lm = hand_landmarks.landmark[identifier]
                return int(lm.x * w), int(lm.y * h)

            thumb_tip = get_point(mp_hands.HandLandmark.THUMB_TIP)
            index_tip = get_point(mp_hands.HandLandmark.INDEX_FINGER_TIP)

            distance = math.hypot(index_tip[0] - thumb_tip[0], index_tip[1] - thumb_tip[1])

            state = 'closed' if distance < DIST_THRESHOLD else 'open'
            if state == 'closed':
                cv2.putText(image, 'Clicked', (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
            if not state_history or state != state_history[-1]:
                state_history.append(state)

            if len(state_history) >= 4 and list(state_history)[-4:] == GESTURE_SEQUENCE:
                gesture_detected = True
                state_history.clear()

            cv2.circle(image, thumb_tip, 10, (0, 0, 255), -1)
            cv2.circle(image, index_tip, 10, (0, 0, 255), -1)
            cv2.line(image, thumb_tip, index_tip, (255, 255, 0), 2)
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    if gesture_detected:
        print("Gesture detected!")
        cv2.putText(image, "Gesture detected!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Gestures', image)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()