import cv2
import mediapipe as mp

# Inicializace mediapipe hands modul
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Funkce pro detekci otevřených a zavřených prstů
def check_fingers(hand_landmarks):
    # Prstová pozice: [1] - palec, [5] - ukazováček, [9] - prostředníček, [13] - prsteníček, [17] - malíček
    finger_tips = [4, 8, 12, 16, 20]  # Pozice prstů
    finger_base = [1, 5, 9, 13, 17]  # Základní klouby prstů
    open_fingers = []

    # Kontrola otevření prstů
    for i in range(5):
        if i == 0:  # Palec
            # Pro palec sledujeme horizontální pohyb a pozici prstu vzhledem k ostatním
            if hand_landmarks.landmark[finger_tips[i]].x > hand_landmarks.landmark[finger_base[i]].x and \
               hand_landmarks.landmark[finger_tips[i]].y < hand_landmarks.landmark[finger_base[i]].y:
                open_fingers.append(i)
        elif i == 4:  # Malíček
            # Pro malíček kontrolujeme vertikální pozici tipového a základního kloubu
            if hand_landmarks.landmark[finger_tips[i]].y < hand_landmarks.landmark[finger_base[i]].y:
                open_fingers.append(i)
        else:
            # Pro ostatní prsty kontrolujeme vertikální pozici
            if hand_landmarks.landmark[finger_tips[i]].y < hand_landmarks.landmark[finger_base[i]].y:
                open_fingers.append(i)

    return open_fingers

# Inicializace kamery
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Převeďte obrázek na RGB pro mediapipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Detekce ruky
    results = hands.process(rgb_frame)

    # Zobrazení detekovaných prstů
    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            # Nakreslení spojnic mezi klouby
            mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

            # Kontrola otevřených prstů
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

    # Zobrazení rámu
    cv2.imshow("Hand Tracking", frame)

    # Ukončení při stisknutí klávesy 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()



"""import cv2
import mediapipe as mp

# Inicializace mediapipe hands modul
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Funkce pro detekci otevřených a zavřených prstů
def check_fingers(hand_landmarks):
    # Prstová pozice: [1] - palec, [5] - ukazováček, [9] - prostředníček, [13] - prsteníček, [17] - malíček
    finger_tips = [4, 8, 12, 16, 20]  # Pozice prstů
    finger_base = [1, 5, 9, 13, 17]  # Základní klouby prstů
    open_fingers = []

    # Kontrola otevření prstů
    for i in range(5):
        if i == 0:  # Palec
            # Pro palec kontrolujeme horizontální vzdálenost mezi tipem a základním kloubem
            if hand_landmarks.landmark[finger_tips[i]].x > hand_landmarks.landmark[finger_base[i]].x:
                open_fingers.append(i)
        elif i == 4:  # Malíček
            # Pro malíček kontrolujeme vertikální pozici a zda se nachází v normální poloze
            if hand_landmarks.landmark[finger_tips[i]].y < hand_landmarks.landmark[finger_base[i]].y:
                open_fingers.append(i)
        else:
            # Pro ostatní prsty kontrolujeme vertikální pozici
            if hand_landmarks.landmark[finger_tips[i]].y < hand_landmarks.landmark[finger_base[i]].y:
                open_fingers.append(i)

    return open_fingers

# Inicializace kamery
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Převeďte obrázek na RGB pro mediapipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Detekce ruky
    results = hands.process(rgb_frame)

    # Zobrazení detekovaných prstů
    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            # Nakreslení spojnic mezi klouby
            mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

            # Kontrola otevřených prstů
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

    # Zobrazení rámu
    cv2.imshow("Hand Tracking", frame)

    # Ukončení při stisknutí klávesy 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()"""


"""import cv2
import mediapipe as mp

# Inicializace mediapipe hands modul
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Funkce pro detekci otevřených a zavřených prstů
def check_fingers(hand_landmarks):
    # Prstová pozice: [1] - palec, [5] - ukazováček, [9] - prostředníček, [13] - prsteníček, [17] - malíček
    finger_tips = [4, 8, 12, 16, 20]  # Pozice prstů
    finger_base = [1, 5, 9, 13, 17]  # Základní klouby prstů

    open_fingers = []

    # Kontrola otevření prstů
    for i in range(5):
        if i == 0:
            # Speciální podmínka pro palec: pro palec sledujeme horizontální pozici (x-ová osa)
            if hand_landmarks.landmark[finger_tips[i]].x > hand_landmarks.landmark[finger_base[i]].x:
                open_fingers.append(i)
        else:
            # Pro ostatní prsty: pokud tip prstu je nad základním kloubem, považujeme prst za otevřený
            if hand_landmarks.landmark[finger_tips[i]].y < hand_landmarks.landmark[finger_base[i]].y:
                open_fingers.append(i)
    
    return open_fingers

# Inicializace kamery
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Převeďte obrázek na RGB pro mediapipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Detekce ruky
    results = hands.process(rgb_frame)

    # Zobrazení detekovaných prstů
    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            # Nakreslení spojnic mezi klouby
            mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

            # Kontrola otevřených prstů
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

    # Zobrazení rámu
    cv2.imshow("Hand Tracking", frame)

    # Ukončení při stisknutí klávesy 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()"""


"""import cv2
import mediapipe as mp

# Inicializace mediapipe hands modul
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Funkce pro detekci otevřených a zavřených prstů
def check_fingers(hand_landmarks):
    # Prstová pozice: [1] - palec, [5] - ukazováček, [9] - prostředníček, [13] - prsteníček, [17] - malíček
    finger_tips = [4, 8, 12, 16, 20]  # Pozice prstů
    finger_base = [1, 5, 9, 13, 17]  # Základní klouby prstů

    open_fingers = []

    # Kontrola otevření prstů
    for i in range(5):
        # Podmínka pro palec: porovnání pozice prstového tipu a kloubu (palec se pohybuje horizontálně)
        if i == 0:
            if hand_landmarks.landmark[finger_tips[i]].x > hand_landmarks.landmark[finger_base[i]].x:
                open_fingers.append(i)
        else:
            # Pro ostatní prsty: pokud tip prstu je nad základním kloubem, považujeme prst za otevřený
            if hand_landmarks.landmark[finger_tips[i]].y < hand_landmarks.landmark[finger_base[i]].y:
                open_fingers.append(i)
    
    return open_fingers

# Inicializace kamery
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Převeďte obrázek na RGB pro mediapipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Detekce ruky
    results = hands.process(rgb_frame)

    # Zobrazení detekovaných prstů
    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            # Nakreslení spojnic mezi klouby
            mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

            # Kontrola otevřených prstů
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

    # Zobrazení rámu
    cv2.imshow("Hand Tracking", frame)

    # Ukončení při stisknutí klávesy 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()"""



"""import cv2
import mediapipe as mp

# Inicializace mediapipe hands modul
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Funkce pro detekci otevřených a zavřených prstů
def check_fingers(hand_landmarks):
    # Prstová pozice: [1] - palec, [5] - ukazováček, [9] - prostředníček, [13] - prsteníček, [17] - malíček
    finger_tips = [4, 8, 12, 16, 20]  # Pozice prstů
    finger_base = [1, 5, 9, 13, 17]  # Základní klouby prstů

    open_fingers = []
    for i in range(5):
        # Zkontrolujeme, zda je prst otevřený
        if hand_landmarks.landmark[finger_tips[i]].y < hand_landmarks.landmark[finger_base[i]].y:
            open_fingers.append(i)
    
    return open_fingers

# Inicializace kamery
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Převeďte obrázek na RGB pro mediapipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Detekce ruky
    results = hands.process(rgb_frame)

    # Zobrazení detekovaných prstů
    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            # Nakreslení spojnic mezi klouby
            mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

            # Kontrola otevřených prstů
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

    # Zobrazení rámu
    cv2.imshow("Hand Tracking", frame)

    # Ukončení při stisknutí klávesy 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()"""