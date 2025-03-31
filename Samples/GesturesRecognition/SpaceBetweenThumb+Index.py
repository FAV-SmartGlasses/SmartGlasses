import cv2
import mediapipe as mp
import math

# Inicializace MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# Kamera
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            h, w, _ = image.shape

            def get_point(id):
                lm = hand_landmarks.landmark[id]
                return int(lm.x * w), int(lm.y * h)

            # Body: špička palce (4), špička ukazováčku (8)
            thumb_tip = get_point(mp_hands.HandLandmark.THUMB_TIP)
            index_tip = get_point(mp_hands.HandLandmark.INDEX_FINGER_TIP)

            # Délka článku ukazováčku: mezi klouby 6 (MCP) a 8 (TIP)
            index_mcp = get_point(mp_hands.HandLandmark.INDEX_FINGER_MCP)
            index_length = math.hypot(index_tip[0] - index_mcp[0], index_tip[1] - index_mcp[1])

            # Vzdálenost mezi palcem a ukazováčkem
            thumb_index_dist = math.hypot(index_tip[0] - thumb_tip[0], index_tip[1] - thumb_tip[1])

            # Zoom metriku
            if index_length > 0:
                zoom_unit = thumb_index_dist / index_length
            else:
                zoom_unit = 0

            # Přibližný odhad v centimetrech (předpokládáme, že článek má cca 5 cm)
            real_distance_cm = (thumb_index_dist / index_length) * 5

            # Vykreslení
            cv2.line(image, thumb_tip, index_tip, (0, 255, 255), 3)
            cv2.circle(image, thumb_tip, 10, (255, 0, 0), -1)
            cv2.circle(image, index_tip, 10, (255, 0, 0), -1)

            cv2.putText(image, f"Zoom unit: {zoom_unit:.2f}", (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            cv2.putText(image, f"Odhad vzdalenosti: {real_distance_cm:.1f} cm", (10, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow('Zoom metrika', image)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()


"""import cv2
import mediapipe as mp
import math

# Inicializace MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# Otevření kamery
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    # Převod na RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    # Pokud jsou detekovány ruce
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Získání souřadnic špičky palce (landmark 4) a ukazováčku (landmark 8)
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            # Převedení relativních souřadnic na pixely
            h, w, _ = image.shape
            thumb_x, thumb_y = int(thumb_tip.x * w), int(thumb_tip.y * h)
            index_x, index_y = int(index_tip.x * w), int(index_tip.y * h)

            # Výpočet vzdálenosti
            distance = math.hypot(index_x - thumb_x, index_y - thumb_y)

            # Zobrazení výsledku
            cv2.putText(image, f"Vzdalenost: {int(distance)} px", (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Kreslení bodů a spojnice
            cv2.circle(image, (thumb_x, thumb_y), 10, (255, 0, 0), -1)
            cv2.circle(image, (index_x, index_y), 10, (255, 0, 0), -1)
            cv2.line(image, (thumb_x, thumb_y), (index_x, index_y), (0, 255, 255), 3)

            # Vykreslení celé ruky
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Zobrazení obrazu
    cv2.imshow('Vzdalenost palec-ukazovacek', image)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC pro ukončení
        break

cap.release()
cv2.destroyAllWindows()"""
