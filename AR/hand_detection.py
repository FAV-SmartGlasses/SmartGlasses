import mediapipe as mp
import cv2
import math
from collections import deque
from menu import Menu

class HandDetection:
    DIST_THRESHOLD = 40  # prahová hodnota pro "spojení prstů"

    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
        self.hand_state_history = deque(maxlen=20)  # ukládá poslední stavy ('open'/'closed')
        self.gesture_detected = False
        self.last_wrist_x = None
        self.current_selection = 0  # aktuálně vybraná položka menu

    def process_image(self, image, w, h, menu_visible, current_selection):
        self.current_selection = current_selection

        results = self.hands.process(image)

        self.gesture_detected = False

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                def get_point(id):
                    lm = hand_landmarks.landmark[id]
                    return int(lm.x * w), int(lm.y * h)
                #neco = self.mp_hands.HandLandmark
                thumb_tip = get_point(self.mp_hands.HandLandmark.THUMB_TIP)
                index_tip = get_point(self.mp_hands.HandLandmark.INDEX_FINGER_TIP)

                #thumb_tip = get_point(neco.THUMB_TIP)
                #thumb_tip = int(neco.THUMB_TIP[0] * w), int(neco.THUMB_TIP[1] * h)
                #index_tip = get_point(neco.INDEX_FINGER_TIP)
                #index_tip = int(neco.INDEX_FINGER_TIP.x * w), int(neco.INDEX_FINGER_TIP.y * h)

                # Vzdálenost mezi palcem a ukazováčkem
                distance = math.hypot(index_tip[0] - thumb_tip[0], index_tip[1] - thumb_tip[1])

                # Detekce "open" / "closed" stavu
                hand_state = 'closed' if distance < self.DIST_THRESHOLD else 'open'
                if not self.hand_state_history or hand_state != self.hand_state_history[-1]:
                    self.hand_state_history.append(hand_state)

                # Sledování pohybu zápěstí pro otevření/zavření menu
                wrist = get_point(self.mp_hands.HandLandmark.WRIST)
                #wrist = int(neco.WRIST.x * w), int(neco.WRIST.y * h)

                # Pokud jsme již zaznamenali poslední pozici zápěstí, zkontrolujeme pohyb
                if self.last_wrist_x is not None:
                    # Pokud zápěstí se pohybuje zleva doprava (otevření menu)
                    if wrist[0] > self.last_wrist_x + 50:  # Pohyb zleva
                        menu_visible = True
                    # Pokud zápěstí se pohybuje zprava doleva (zavření menu)
                    elif wrist[0] < self.last_wrist_x - 50:  # Pohyb zprava
                        menu_visible = False

                # Uložení poslední pozice zápěstí
                self.last_wrist_x = wrist[0]

                if menu_visible:
                    self.DetectMenuItemSelection(h, thumb_tip, index_tip)  # Získání aktuálního výběru položky menu
                    menu_visible = self.CheckClickGestureForOpeningApp(hand_state, menu_visible)  # Kontrola gesta pro otevření aplikace

                self.draw(w, image, hand_landmarks, thumb_tip, index_tip)   #nakreslí čáry a body na ruce

        return image, menu_visible, self.current_selection

    def get_point(self, hand_landmarks, id, w, h):
        lm = hand_landmarks.landmark[id]
        return int(lm.x * w), int(lm.y * h)

    """def get_point(self, hand_landmarks, w, h):
        lm = hand_landmarks #.landmark[id]
        return int(lm.x * w), int(lm.y * h)"""
    
    def DetectMenuItemSelection(self, h, thumb_tip, index_tip):
        menu_width = 300
        menu_height = 300
        padding = 20
        menu_x = 10
        menu_y = h // 2 - menu_height // 2
        for i, item in enumerate(Menu.items):
            item_x = menu_x + padding
            item_y = menu_y + padding + i * (menu_height // len(Menu.items))
            item_height = 40  # výška tlačítka
            middle_point_y = (thumb_tip[1] + index_tip[1]) // 2
            if item_y <= middle_point_y <= item_y + item_height:
                self.current_selection = i  # označ aktuálně vybrané tlačítko
                # volitelně: zvýraznění nebo výpis
                print(f"Zelená čára ukazuje na: {Menu.items[i].get_name()}")

    def CheckClickGestureForOpeningApp(self, hand_state, menu_visible):
        """if hand_state == 'closed':
            if self.current_selection == len(Menu.menu_items) - 1:  # Poslední položka = zavření menu
                menu_visible = False  # zavření menu
            else:
                print(f"Spuštěná aplikace: {Menu.menu_items[self.current_selection]}")
                menu_visible = False"""
        # otevření app nebo zavření
        if hand_state == 'closed':
            menu_visible = False
            if self.current_selection != len(Menu.items) - 1:  #kdyč to není poslední položka menu
                print(f"Spuštěná aplikace: {Menu.items[self.current_selection].get_name()}")
        return menu_visible
            
    
    def draw(self, w, image, hand_landmarks, thumb_tip, index_tip):
        # Vytvoření bodu mezi palcem a ukazováčkem (polovina mezi těmito dvěma body)
        middle_point_x = (thumb_tip[0] + index_tip[0]) // 2
        middle_point_y = (thumb_tip[1] + index_tip[1]) // 2
        # Kreslení bodu mezi palcem a ukazováčkem (červený bod)
        cv2.circle(image, (middle_point_x, middle_point_y), 10, (0, 0, 255), -1)
        # Kreslení vodorovné čáry v místě bodu mezi palcem a ukazováčkem (zelená čára)
        cv2.line(image, (0, middle_point_y), (w, middle_point_y), (0, 255, 0), 2)  # Zelená čára

        # Kreslení ruky a pozic
        cv2.circle(image, thumb_tip, 10, (0, 0, 255), -1)
        cv2.circle(image, index_tip, 10, (0, 0, 255), -1)
        cv2.line(image, thumb_tip, index_tip, (255, 255, 0), 2)
        self.mp_drawing.draw_landmarks(image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)