import cv2
import mediapipe as mp
import math

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

def calculate_distance_3d(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2 + (point1.z - point2.z) ** 2)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            for point in landmarks.landmark:
                x = int(point.x * frame.shape[1])
                y = int(point.y * frame.shape[0])
                cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)

            thumb_tip = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_tip = landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            ring_tip = landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
            pinky_tip = landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

            thumb_index_distance = calculate_distance_3d(thumb_tip, index_tip)
            index_middle_distance = calculate_distance_3d(index_tip, middle_tip)
            middle_ring_distance = calculate_distance_3d(middle_tip, ring_tip)
            ring_pinky_distance = calculate_distance_3d(ring_tip, pinky_tip)

            if (thumb_index_distance < 0.05 and index_middle_distance < 0.05
                and middle_ring_distance < 0.05 and ring_pinky_distance < 0.05):
                
                cv2.putText(frame, "Pest Detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "No Pest", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Hand Gesture Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()