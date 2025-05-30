import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

def check_fingers(hand_landmarks):
    finger_tips = [4, 8, 12, 16, 20]
    finger_base = [1, 5, 9, 13, 17]
    open_fingers = []

    for i in range(5):
        if i == 0:
            if hand_landmarks.landmark[finger_tips[i]].x > hand_landmarks.landmark[finger_base[i]].x and \
               hand_landmarks.landmark[finger_tips[i]].y < hand_landmarks.landmark[finger_base[i]].y:
                open_fingers.append(i)
        elif i == 4:
            if hand_landmarks.landmark[finger_tips[i]].y < hand_landmarks.landmark[finger_base[i]].y:
                open_fingers.append(i)
        else:
            if hand_landmarks.landmark[finger_tips[i]].y < hand_landmarks.landmark[finger_base[i]].y:
                open_fingers.append(i)

    return open_fingers

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

            open_fingers = check_fingers(landmarks)
            for finger in open_fingers:
                if finger == 0:
                    cv2.putText(frame, "Thumb: Open", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                elif finger == 1:
                    cv2.putText(frame, "Index: Open", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                elif finger == 2:
                    cv2.putText(frame, "Middle: Open", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                elif finger == 3:
                    cv2.putText(frame, "Ring: Open", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                elif finger == 4:
                    cv2.putText(frame, "Pinky: Open", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Hand Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()