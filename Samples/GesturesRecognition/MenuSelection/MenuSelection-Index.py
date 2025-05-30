import cv2
import mediapipe as mp
import math

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

def angle_between_points(p1, p2, p3):
    v1 = (p1.x - p2.x, p1.y - p2.y)
    v2 = (p3.x - p2.x, p3.y - p2.y)

    if (v1[0] == 0 and v1[1] == 0) or (v2[0] == 0 and v2[1] == 0):
        return 0

    dot_product = v1[0] * v2[0] + v1[1] * v2[1]
    magnitude_v1 = math.sqrt(v1[0]**2 + v1[1]**2)
    magnitude_v2 = math.sqrt(v2[0]**2 + v2[1]**2)
    
    if magnitude_v1 == 0 or magnitude_v2 == 0:
        return 0

    cos_angle = dot_product / (magnitude_v1 * magnitude_v2)
    angle_rad = math.acos(cos_angle)
    angle_deg = math.degrees(angle_rad)
    return angle_deg

while cap.isOpened():
    success, img = cap.read()
    if not success:
        break

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            index_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]

            x_tip = int(index_tip.x * img.shape[1])
            x_mcp = int(index_mcp.x * img.shape[1])
            y_tip = int(index_tip.y * img.shape[0])
            y_mcp = int(index_mcp.y * img.shape[0])

            dx = x_tip - x_mcp
            dy = y_mcp - y_tip

            angle_rad = math.atan2(dy, dx)
            angle_deg = math.degrees(angle_rad)
            if angle_deg < 0:
                angle_deg += 360

            if 350 <= angle_deg or angle_deg < 10:
                direction = "Right"
            elif 80 <= angle_deg < 100:
                direction = "Up"
            elif 170 <= angle_deg < 190:
                direction = "Left"
            elif 260 <= angle_deg < 280:
                direction = "Down"
            else:
                direction = ""

            cv2.putText(img, f"Angle: {angle_deg:.1f}°", (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (255, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(img, f"Direction: {direction}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 255), 2, cv2.LINE_AA)
            
            index_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
            index_pip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]
            index_dip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP]

            index_angle = angle_between_points(index_mcp, index_pip, index_dip)

            index_open = index_angle > 160

            other_fingers_closed = True

            for finger in [mp_hands.HandLandmark.MIDDLE_FINGER_MCP, mp_hands.HandLandmark.RING_FINGER_MCP, mp_hands.HandLandmark.PINKY_MCP]:
                finger_mcp = hand_landmarks.landmark[finger]
                finger_pip = hand_landmarks.landmark[finger + 1] if finger + 1 < len(hand_landmarks.landmark) else None
                if finger_pip:
                    finger_angle = angle_between_points(finger_mcp, finger_pip, finger_pip)
                    if finger_angle > 160:
                        other_fingers_closed = False

            if direction == "Left" or direction == "Right":
                if index_open and other_fingers_closed:
                    cv2.putText(img, "Index Finger Opened", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            
            if (direction == "Left" or direction == "Right") and index_open and other_fingers_closed:
                y_position = int(index_tip.y * img.shape[0])

                cv2.line(img, (0, y_position), (img.shape[1], y_position), (0, 255, 0), 2)

    cv2.imshow("Hand Tracking", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()