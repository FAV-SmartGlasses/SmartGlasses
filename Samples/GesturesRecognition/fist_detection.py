import cv2
import mediapipe as mp
import math

# Inicializace MediaPipe Hand modelu
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Otevření kamery
cap = cv2.VideoCapture(0)

def calculate_distance_3d(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2 + (point1.z - point2.z) ** 2)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Obrátit barvy (OpenCV používá BGR, ale MediaPipe očekává RGB)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Detekce ruky
    results = hands.process(frame_rgb)

    # Pokud jsou detekovány ruce
    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            # Pišeme souřadnice bodů ruky
            for point in landmarks.landmark:
                x = int(point.x * frame.shape[1])
                y = int(point.y * frame.shape[0])
                cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)

            # Zjištění, zda je ukázaná pěst
            # Používáme vzdálenosti mezi prsty, abychom zjistili, zda jsou všechny prsty spojené (pěst)
            thumb_tip = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_tip = landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            ring_tip = landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
            pinky_tip = landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

            # Vypočteme vzdálenosti mezi prsty pomocí 3D souřadnic
            thumb_index_distance = calculate_distance_3d(thumb_tip, index_tip)
            index_middle_distance = calculate_distance_3d(index_tip, middle_tip)
            middle_ring_distance = calculate_distance_3d(middle_tip, ring_tip)
            ring_pinky_distance = calculate_distance_3d(ring_tip, pinky_tip)

            # Pokud jsou vzdálenosti mezi prsty malé, pravděpodobně ukazuješ pěst
            # Zde přidáváme větší toleranci pro různé úhly a vzdálenost ruky
            if (thumb_index_distance < 0.05 and index_middle_distance < 0.05 
                and middle_ring_distance < 0.05 and ring_pinky_distance < 0.05):
                
                cv2.putText(frame, "Pest Detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "No Pest", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Zobrazíme obrázek s detekcí
    cv2.imshow("Hand Gesture Recognition", frame)

    # Zastavíme kameru pokud stiskneme 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Uvolnění kamery a zavření oken
cap.release()
cv2.destroyAllWindows()


"""import cv2
import mediapipe as mp
import math

# Inicializace MediaPipe Hand modelu
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Otevření kamery
cap = cv2.VideoCapture(0)

def calculate_distance(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Obrátit barvy (OpenCV používá BGR, ale MediaPipe očekává RGB)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Detekce ruky
    results = hands.process(frame_rgb)

    # Pokud jsou detekovány ruce
    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            # Pišeme souřadnice bodů ruky
            for point in landmarks.landmark:
                x = int(point.x * frame.shape[1])
                y = int(point.y * frame.shape[0])
                cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)

            # Zjištění, zda je ukázaná pěst
            # Používáme vzdálenosti mezi prsty, aby jsme zjistili, zda jsou všechny prsty spojené (pěst)
            thumb_tip = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_tip = landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            ring_tip = landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
            pinky_tip = landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

            # Vypočteme vzdálenosti mezi prsty
            thumb_index_distance = calculate_distance(thumb_tip, index_tip)
            index_middle_distance = calculate_distance(index_tip, middle_tip)
            middle_ring_distance = calculate_distance(middle_tip, ring_tip)
            ring_pinky_distance = calculate_distance(ring_tip, pinky_tip)

            # Pokud jsou vzdálenosti mezi prsty malé, pravděpodobně ukazuješ pěst
            # Zde přidáváme větší toleranci pro různé úhly
            if (thumb_index_distance < 0.05 and index_middle_distance < 0.05 
                and middle_ring_distance < 0.05 and ring_pinky_distance < 0.05):
                
                cv2.putText(frame, "Pest Detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "No Pest", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Zobrazíme obrázek s detekcí
    cv2.imshow("Hand Gesture Recognition", frame)

    # Zastavíme kameru pokud stiskneme 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Uvolnění kamery a zavření oken
cap.release()
cv2.destroyAllWindows()"""



"""import cv2
import mediapipe as mp

# Inicializace MediaPipe Hand modelu
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Otevření kamery
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Obrátit barvy (OpenCV používá BGR, ale MediaPipe očekává RGB)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Detekce ruky
    results = hands.process(frame_rgb)

    # Pokud jsou detekovány ruce
    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            # Pišeme souřadnice bodů ruky
            for point in landmarks.landmark:
                x = int(point.x * frame.shape[1])
                y = int(point.y * frame.shape[0])
                cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)

            # Zjištění, zda je ukázaná pěst
            # Používáme vzdálenost mezi jednotlivými prsty, aby jsme zjistili, zda jsou všechny prsty spojené (pěst)
            thumb_tip = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_tip = landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            ring_tip = landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
            pinky_tip = landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

            # Vypočteme vzdálenosti mezi prsty
            thumb_index_distance = ((thumb_tip.x - index_tip.x) ** 2 + (thumb_tip.y - index_tip.y) ** 2) ** 0.5
            index_middle_distance = ((index_tip.x - middle_tip.x) ** 2 + (index_tip.y - middle_tip.y) ** 2) ** 0.5
            middle_ring_distance = ((middle_tip.x - ring_tip.x) ** 2 + (middle_tip.y - ring_tip.y) ** 2) ** 0.5
            ring_pinky_distance = ((ring_tip.x - pinky_tip.x) ** 2 + (ring_tip.y - pinky_tip.y) ** 2) ** 0.5

            # Pokud jsou vzdálenosti mezi prsty malé, pravděpodobně ukazuješ pěst
            if thumb_index_distance < 0.05 and index_middle_distance < 0.05 and middle_ring_distance < 0.05 and ring_pinky_distance < 0.05:
                cv2.putText(frame, "Pest Detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Zobrazíme obrázek s detekcí
    cv2.imshow("Hand Gesture Recognition", frame)

    # Zastavíme kameru pokud stiskneme 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Uvolnění kamery a zavření oken
cap.release()
cv2.destroyAllWindows()"""