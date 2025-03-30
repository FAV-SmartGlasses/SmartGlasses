import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, img = cap.read()
    if not success:
        break

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Kreslení základních linií ruky
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Získání pozic jednotlivých bodů na ukazováčku
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]

            # Porovnání pozice ukazováčku s zápěstím
            if index_finger_tip.x < wrist.x:  # Pokud je ukazováček vlevo od zápěstí
                # Zjištění výšky ukazováčku
                y_position = int(index_finger_tip.y * img.shape[0])

                # Nakreslení čáry na tuto výšku
                cv2.line(img, (0, y_position), (img.shape[1], y_position), (0, 255, 0), 2)

    # Zobrazení výsledného obrázku
    cv2.imshow("Hand Tracking", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()