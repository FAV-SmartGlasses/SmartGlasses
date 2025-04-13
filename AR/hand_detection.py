import mediapipe as mp
import cv2
import math
from collections import deque
from enum import Enum
from config import *

class HandDetection:
    DIST_THRESHOLD = 40  # prahová hodnota pro "spojení prstů"

    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
        self.click_gesture_history = deque(maxlen=20)  # ukládá poslední stavy
        self.last_wrist_x = None
        self.last_wrist_y = None

    def process_image(self, image, w, h):
        results = self.hands.process(image)

        click_gesture_detected = False
        swipe_gesture_detected = self.SwipeGesture.NO
        cursor_position = None, None

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                click_gesture_detected = self.is_click_gesture_detected(hand_landmarks, w, h)  # Kontrola gesta pro kliknutí

                swipe_gesture_detected = self.swipe_gesture_detected(hand_landmarks, w, h)  # Kontrola gesta pro posun

                cursor_position = self.get_cursor_position(image, w, h)  # Získání pozice kurzoru

                #TODO: add gesture for moving and resizing apps

                self.draw(w, h, image, hand_landmarks)   #nakreslí čáry a body na ruce

        #self.hands.close()

        return image, click_gesture_detected, swipe_gesture_detected, cursor_position
    
    class SwipeGesture(Enum):
        NO = 0
        RIGHT = 1
        LEFT = 2
        DOWN = 3
        UP = 4

    def swipe_gesture_detected(self, hand_landmarks, w, h):
        wrist = self.get_wrist(hand_landmarks, w, h)  # Získání pozice zápěstí

        # Pokud jsme již zaznamenali poslední pozici zápěstí, zkontrolujeme pohyb
        if self.last_wrist_x is not None:
            if wrist[0] > self.last_wrist_x + 50:
                gesture_detected = self.SwipeGesture.RIGHT
                print("Swipe right")
            elif wrist[0] < self.last_wrist_x - 50:
                gesture_detected = self.SwipeGesture.LEFT
                print("Swipe left")
            else:
                gesture_detected = self.SwipeGesture.NO
                #print("No swipe gesture detected")
        else:
            gesture_detected = self.SwipeGesture.NO

        self.last_wrist_x = wrist[0] # Uložení poslední pozice zápěstí

        return gesture_detected

    def is_click_gesture_detected(self, hand_landmarks, w, h):
        thumb_tip = self.get_thumb_tip(hand_landmarks, w, h)  # Získání pozice palce
        index_tip = self.get_index_tip(hand_landmarks, w, h)  # Získání pozice ukazováčku

        distance = math.hypot(index_tip[0] - thumb_tip[0], index_tip[1] - thumb_tip[1]) # Vzdálenost mezi palcem a ukazováčkem

        # Detekce stavu spojení palce a ukazováčku
        click_gesture_detected = True if distance < self.DIST_THRESHOLD else False
        if not self.click_gesture_history or click_gesture_detected != self.click_gesture_history[-1]:
            self.click_gesture_history.append(click_gesture_detected)

        return click_gesture_detected

    def get_point(self, id, hand_landmarks, w, h):
        lm = hand_landmarks.landmark[id]
        return int(lm.x * w), int(lm.y * h)

    def get_thumb_tip(self, hand_landmarks, w, h):
        mp_hands = mp.solutions.hands
        return self.get_point(mp_hands.HandLandmark.THUMB_TIP, hand_landmarks, w, h)
    
    def get_index_tip(self, hand_landmarks, w, h):
        mp_hands = mp.solutions.hands
        return self.get_point(mp_hands.HandLandmark.INDEX_FINGER_TIP, hand_landmarks, w, h)
    
    def get_wrist(self, hand_landmarks, w, h):
        mp_hands = mp.solutions.hands
        return self.get_point(mp_hands.HandLandmark.WRIST, hand_landmarks, w, h)
    
    def get_cursor_position(self, image, w, h):
        results = self.hands.process(image)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                thumb_tip = self.get_thumb_tip(hand_landmarks, w, h)  # Získání pozice palce
                index_tip = self.get_index_tip(hand_landmarks, w, h)  # Získání pozice ukazováčku

                middle_point_x = (thumb_tip[0] + index_tip[0]) // 2
                middle_point_y = (thumb_tip[1] + index_tip[1]) // 2

                return middle_point_x, middle_point_y
        return None, None

    def draw(self, w, h, image, hand_landmarks):
        thumb_tip = self.get_thumb_tip(hand_landmarks, w, h)  # Získání pozice palce
        index_tip = self.get_index_tip(hand_landmarks, w, h)  # Získání pozice ukazováčku

        # Vytvoření bodu mezi palcem a ukazováčkem (polovina mezi těmito dvěma body)
        middle_point_x = (thumb_tip[0] + index_tip[0]) // 2
        middle_point_y = (thumb_tip[1] + index_tip[1]) // 2

        # Kreslení kurzoru - bodu mezi palcem a ukazováčkem (červený bod)
        cv2.circle(image, (middle_point_x, middle_point_y), 10, (0, 0, 255), -1)

        if DRAW_GREEN_LINE_FOR_MENU_SELECTION:
            # Kreslení vodorovné čáry v místě bodu mezi palcem a ukazováčkem (zelená čára)
            cv2.line(image, (0, middle_point_y), (w, middle_point_y), (0, 255, 0), 2)  # Zelená čára

        if SHOW_FINGER_JOINTS:
            # Kreslení ruky a pozic
            cv2.circle(image, thumb_tip, 10, (0, 0, 255), -1)
            cv2.circle(image, index_tip, 10, (0, 0, 255), -1)
            cv2.line(image, thumb_tip, index_tip, (255, 255, 0), 2)
            self.mp_drawing.draw_landmarks(image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)