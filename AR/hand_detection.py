import mediapipe as mp
import cv2
import math
from collections import deque
from enum import Enum
from config import *

class HandDetection:
    DIST_THRESHOLD = 40  # finger touch threshold

    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
        self.click_gesture_history = deque(maxlen=20)  # save the last states
        self.last_wrist_x = None
        self.last_wrist_y = None

    def process_image(self, image, w, h):
        results = self.hands.process(image)

        click_gesture_detected = False
        swipe_gesture_detected = self.SwipeGesture.NO
        cursor_position = None, None

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                click_gesture_detected = self.is_click_gesture_detected(hand_landmarks, w, h)  # Check for click gesture

                swipe_gesture_detected = self.swipe_gesture_detected(hand_landmarks, w, h)  # Check for swipe gesture

                cursor_position = self.get_cursor_position(image, w, h)  # Get cursor position

                # TODO: add gesture for moving and resizing apps

                self.draw(w, h, image, hand_landmarks)  # Draw lines and points on the hand

        #self.hands.close()

        return image, click_gesture_detected, swipe_gesture_detected, cursor_position
    
    class SwipeGesture(Enum):
        NO = 0
        RIGHT = 1
        LEFT = 2
        DOWN = 3
        UP = 4

    def swipe_gesture_detected(self, hand_landmarks, w, h):
        wrist = self.get_wrist(hand_landmarks, w, h)  # Get wrist position

        # If the last wrist position is already recorded, check for movement
        if self.last_wrist_x is not None and self.last_wrist_y is not None:
            delta_x = wrist[0] - self.last_wrist_x
            delta_y = wrist[1] - self.last_wrist_y

            # Threshold for movement detection
            threshold = 50

            if abs(delta_x) > abs(delta_y):  # Horizontal movement
                if delta_x > threshold:
                    gesture_detected = self.SwipeGesture.RIGHT
                    print("Swipe right")
                elif delta_x < -threshold:
                    gesture_detected = self.SwipeGesture.LEFT
                    print("Swipe left")
                else:
                    gesture_detected = self.SwipeGesture.NO
            else:  # Vertical movement
                if delta_y > threshold:
                    gesture_detected = self.SwipeGesture.DOWN
                    print("Swipe down")
                elif delta_y < -threshold:
                    gesture_detected = self.SwipeGesture.UP
                    print("Swipe up")
                else:
                    gesture_detected = self.SwipeGesture.NO
        else:
            gesture_detected = self.SwipeGesture.NO

        # Save the last wrist position
        self.last_wrist_x = wrist[0]
        self.last_wrist_y = wrist[1]

        return gesture_detected

    def is_click_gesture_detected(self, hand_landmarks, w, h):
        thumb_tip = self.get_thumb_tip(hand_landmarks, w, h)  # Get thumb position
        index_tip = self.get_index_tip(hand_landmarks, w, h)  # Get index finger position

        distance = math.hypot(index_tip[0] - thumb_tip[0], index_tip[1] - thumb_tip[1])  # Distance between thumb and index finger

        # Detect the state of thumb and index finger touching
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
                thumb_tip = self.get_thumb_tip(hand_landmarks, w, h)  # Get thumb position
                index_tip = self.get_index_tip(hand_landmarks, w, h)  # Get index finger position

                middle_point_x = (thumb_tip[0] + index_tip[0]) // 2
                middle_point_y = (thumb_tip[1] + index_tip[1]) // 2

                return middle_point_x, middle_point_y
        return None, None

    def draw(self, w, h, image, hand_landmarks):
        thumb_tip = self.get_thumb_tip(hand_landmarks, w, h)  # Get thumb position
        index_tip = self.get_index_tip(hand_landmarks, w, h)  # Get index finger position

        # Create a point between thumb and index finger (midpoint between these two points)
        middle_point_x = (thumb_tip[0] + index_tip[0]) // 2
        middle_point_y = (thumb_tip[1] + index_tip[1]) // 2

        # Draw the cursor - a point between thumb and index finger (red dot)
        cv2.circle(image, (middle_point_x, middle_point_y), 10, (0, 0, 255), -1)

        if DRAW_GREEN_LINE_FOR_MENU_SELECTION:
            # Draw a horizontal line at the point between thumb and index finger (green line)
            cv2.line(image, (0, middle_point_y), (w, middle_point_y), (0, 255, 0), 2)  # Green line

        if SHOW_FINGER_JOINTS:
            # Draw the hand and positions
            cv2.circle(image, thumb_tip, 10, (0, 0, 255), -1)
            cv2.circle(image, index_tip, 10, (0, 0, 255), -1)
            cv2.line(image, thumb_tip, index_tip, (255, 255, 0), 2)
            self.mp_drawing.draw_landmarks(image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)