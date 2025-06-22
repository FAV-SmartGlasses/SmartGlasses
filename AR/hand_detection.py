import math
from collections import deque

import cv2
import time
import mediapipe as mp
import numpy as np

from config import *
from hand_detection_models import *


def calculate_distance_3d(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2 + (point1.z - point2.z) ** 2)


def combine_swipe_gestures(left_gesture: SwipeGesture, right_gesture: SwipeGesture):
    if left_gesture == SwipeGesture.RIGHT and right_gesture == SwipeGesture.RIGHT:
        return SwipeGesture.BOTH_RIGHT
    elif left_gesture == SwipeGesture.LEFT and right_gesture == SwipeGesture.LEFT:
        return SwipeGesture.BOTH_LEFT
    elif left_gesture == SwipeGesture.LEFT and right_gesture == SwipeGesture.RIGHT:
        return SwipeGesture.BOTH_OUT
    elif left_gesture == SwipeGesture.RIGHT and right_gesture == SwipeGesture.LEFT:
        return SwipeGesture.BOTH_IN
    elif left_gesture != SwipeGesture.NO and right_gesture == SwipeGesture.NO:
        return left_gesture
    elif left_gesture == SwipeGesture.NO and right_gesture != SwipeGesture.NO:
        return right_gesture
    else:
        return SwipeGesture.NO


def get_point(id_, hand_landmarks, w, h) -> Position:
    lm = hand_landmarks.landmark[id_]
    return Position(int(lm.x * w), int(lm.y * h))


class HandDetection:
    CLICK_DIST_THRESHOLD = 40  # finger touch threshold
    FIST_FINGER_DISTANCE_THRESHOLD = 0.05
    SWIPE_SPEED_THRESHOLD = 500  # px/s
    SWIPE_DISTANCE_THRESHOLD = 50  # px – MIN distance to consider a swipe
    SWIPE_COOLDOWN = 0.3  # 300 ms cooldown between 2 swipe gestures

    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7)
        
        self.click_gesture_history = deque(maxlen=20)  # save the last states

        self.last_left_wrist: Position = Position()
        self.last_right_wrist: Position = Position()

        self.last_left_fist_detected: bool = False
        self.last_right_fist_detected: bool = False

        self.last_left_wrist_time = 0
        self.last_right_wrist_time = 0
        self.last_swipe_time = 0

        self.last_left_cursor_position: Position = Position()
        self.last_right_cursor_position: Position = Position()


    def draw(self, image: np.ndarray, hand_landmarks):
        h, w, _ = image.shape

        thumb_tip = self.get_thumb_tip(hand_landmarks, w, h)  # Get thumb position
        index_tip = self.get_index_tip(hand_landmarks, w, h)  # Get index finger position

        cursor = self.get_cursor_position(w, h, hand_landmarks)

        # Draw the cursor - a point between thumb and index finger (red dot)
        cv2.circle(image, cursor.get_array(), 10, (0, 0, 255), -1)

        if DRAW_GREEN_LINE_FOR_MENU_SELECTION:
            # Draw a horizontal line at the point between thumb and index finger (green line)
            cv2.line(image, (0, cursor.y), (w, cursor.y), (0, 255, 0), 2)  # Green line

        if SHOW_FINGER_JOINTS:
            # Draw the hand and positions
            cv2.circle(image, thumb_tip.get_array(), 10, (0, 0, 255), -1)
            cv2.circle(image, index_tip.get_array(), 10, (0, 0, 255), -1)
            cv2.line(image, thumb_tip.get_array(), index_tip.get_array(), (255, 255, 0), 2)
            self.mp_drawing.draw_landmarks(image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

    def process_image(self, image: np.ndarray) -> tuple[np.ndarray, DetectionModel]:
        h, w, _ = image.shape

        hands_results = self.hands.process(image)
        # to create MEMORY LEAK: creating new instance of MediaPipe Hands at every frame
        #hands_instance = self.mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7)
        #hands_results = hands_instance.process(image)
        # hands_instance.close()  # this code is avoiding memory leak if 2 previus lines are uncommented

        result = DetectionModel()
        left_swipe_gesture_detected = SwipeGesture.NO
        right_swipe_gesture_detected = SwipeGesture.NO

        left_hand, right_hand = None, None
        hand_landmarks_list = hands_results.multi_hand_landmarks
        handedness_list = getattr(hands_results, 'multi_handedness', None)
        if hand_landmarks_list:
            if len(hand_landmarks_list) == 2:
                if USE_MEDIAPIPE_HANDEDNESS and handedness_list:
                    # Určení podle MediaPipe
                    hand_labels = [h.classification[0].label for h in handedness_list]
                    # Najít indexy levé a pravé ruky
                    try:
                        left_idx = hand_labels.index("Left")
                        right_idx = hand_labels.index("Right")
                        left_hand = hand_landmarks_list[left_idx]
                        right_hand = hand_landmarks_list[right_idx]
                    except ValueError:
                        # fallback na pozici pokud by MediaPipe nevrátil obě
                        left_hand, right_hand = self.get_left_and_right_hands(hand_landmarks_list, w, h)
                else:
                    # Určení podle pozice (x-ové souřadnice)
                    left_hand, right_hand = self.get_left_and_right_hands(hand_landmarks_list, w, h)

                result.left_hand.fist = self.is_fist_detected(left_hand)
                result.right_hand.fist = self.is_fist_detected(right_hand)
                if result.left_hand.fist and result.right_hand.fist:
                    result.left_hand.fist = result.right_hand.fist = False

                left_swipe_gesture_detected = self.swipe_gesture_detected(left_hand, w, h, is_left = True)
                right_swipe_gesture_detected = self.swipe_gesture_detected(right_hand, w, h, is_left = False)

                result.left_hand.clicked = self.is_click_gesture_detected(left_hand, w, h)
                result.right_hand.clicked = self.is_click_gesture_detected(right_hand, w, h)

                result.left_hand.cursor = self.get_cursor_position(w, h, left_hand)
                result.right_hand.cursor = self.get_cursor_position(w, h, right_hand)

                self.draw(image, left_hand)
                self.draw(image, right_hand)
            elif len(hand_landmarks_list) == 1:
                right_hand = hand_landmarks_list[0]

                result.right_hand.fist = self.is_fist_detected(right_hand)

                right_swipe_gesture_detected = self.swipe_gesture_detected(right_hand, w, h, is_left=False)
                result.right_hand.clicked = self.is_click_gesture_detected(right_hand, w, h)
                result.right_hand.cursor = self.get_cursor_position(w, h, right_hand)
                self.draw(image, right_hand)
            elif len(hand_landmarks_list) == 0:
                result.right_hand.cursor = Position()
                result.left_hand.cursor = Position()

        result.left_hand.last_wrist_position = self.last_left_wrist
        result.right_hand.last_wrist_position = self.last_right_wrist

        result.left_hand.last_cursor_position = self.last_left_cursor_position
        result.right_hand.last_cursor_position = self.last_right_cursor_position
        self.last_left_fist_detected = result.left_hand.fist
        self.last_right_fist_detected = result.right_hand.fist
        self.last_left_cursor_position = result.left_hand.cursor
        self.last_right_cursor_position = result.right_hand.cursor

        # Save the last wrist position
        if left_hand is not None:
            self.last_left_wrist = result.left_hand.wrist_position = self.get_wrist(left_hand, w, h)
        else:
            self.last_left_wrist = result.left_hand.wrist_position = Position()
        if right_hand is not None:
            self.last_right_wrist = result.right_hand.wrist_position = self.get_wrist(right_hand, w, h)
        else:
            self.last_right_wrist = result.right_hand.wrist_position = Position()
            #print("No right hand detected")

        if result.left_hand.clicked and result.right_hand.clicked:
            result.left_hand.clicked = False
            result.right_hand.clicked = False

        """if right_swipe_gesture_detected == SwipeGesture.RIGHT:
                print("neco")"""

        result.swipe = combine_swipe_gestures(left_swipe_gesture_detected, right_swipe_gesture_detected)

        if PRINT_SWIPE_GESTURES and result.swipe is not SwipeGesture.NO:
            print(f"Swipe gesture detected: {result.swipe.name}")

        return image, result


    def is_fist_detected(self, hand_landmarks) -> bool:
        #getting positions of every finger
        thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
        index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        middle_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        ring_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP]
        pinky_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_TIP]

        # calculating distances between fingers with 3D coordinates
        thumb_index_distance = calculate_distance_3d(thumb_tip, index_tip)
        index_middle_distance = calculate_distance_3d(index_tip, middle_tip)
        middle_ring_distance = calculate_distance_3d(middle_tip, ring_tip)
        ring_pinky_distance = calculate_distance_3d(ring_tip, pinky_tip)

        # if distances between fingers are smaller than DISTANCE_THRESHOLD, fist gesture is detected
        return (thumb_index_distance < self.FIST_FINGER_DISTANCE_THRESHOLD and index_middle_distance < self.FIST_FINGER_DISTANCE_THRESHOLD and
                middle_ring_distance < self.FIST_FINGER_DISTANCE_THRESHOLD and ring_pinky_distance < self.FIST_FINGER_DISTANCE_THRESHOLD)

    def swipe_gesture_detected(self, hand_landmarks, w, h, is_left):
        wrist = self.get_wrist(hand_landmarks, w, h)
        current_time = time.time()

        # Bezpečné čtení pozic
        wrist_x = wrist.x if wrist.x is not None else 0
        wrist_y = wrist.y if wrist.y is not None else 0

        if is_left:
            last_pos = self.last_left_wrist
            last_time = self.last_left_wrist_time
        else:
            last_pos = self.last_right_wrist
            last_time = self.last_right_wrist_time

        last_x = last_pos.x if last_pos.x is not None else 0
        last_y = last_pos.y if last_pos.y is not None else 0

        # První frame – nastav pouze poslední pozici a čas
        if last_time == 0 or (last_pos.x is None or last_pos.y is None):
            if is_left:
                self.last_left_wrist = wrist
                self.last_left_wrist_time = current_time
            else:
                self.last_right_wrist = wrist
                self.last_right_wrist_time = current_time
            return SwipeGesture.NO

        delta_time = current_time - last_time
        if delta_time == 0:
            return SwipeGesture.NO

        delta_x = wrist_x - last_x
        delta_y = wrist_y - last_y

        speed_x = delta_x / delta_time
        speed_y = delta_y / delta_time

        gesture = SwipeGesture.NO

        # Vyhodnocení směru jen pokud překročena rychlost i vzdálenost
        if abs(speed_x) > abs(speed_y) and abs(delta_x) > self.SWIPE_DISTANCE_THRESHOLD:
            if speed_x > self.SWIPE_SPEED_THRESHOLD:
                gesture = SwipeGesture.RIGHT
            elif speed_x < -self.SWIPE_SPEED_THRESHOLD:
                gesture = SwipeGesture.LEFT
        elif abs(speed_y) > abs(speed_x) and abs(delta_y) > self.SWIPE_DISTANCE_THRESHOLD:
            if speed_y > self.SWIPE_SPEED_THRESHOLD:
                gesture = SwipeGesture.DOWN
            elif speed_y < -self.SWIPE_SPEED_THRESHOLD:
                gesture = SwipeGesture.UP

        # Cooldown proti opakování
        if current_time - self.last_swipe_time < self.SWIPE_COOLDOWN:
            gesture = SwipeGesture.NO
        elif gesture != SwipeGesture.NO:
            self.last_swipe_time = current_time

        # Ulož novou pozici
        if is_left:
            self.last_left_wrist = wrist
            self.last_left_wrist_time = current_time
        else:
            self.last_right_wrist = wrist
            self.last_right_wrist_time = current_time

        if gesture != SwipeGesture.NO:
            print(f"{'Left' if is_left else 'Right'} hand swipe {gesture.name.lower()}")

        return gesture


    def get_left_and_right_hands(self, hand_landmarks_list, w, h):
        hand_1_wrist = self.get_wrist(hand_landmarks_list[0], w, h)
        hand_2_wrist = self.get_wrist(hand_landmarks_list[1], w, h)

        #returning hands in order: left, right
        if hand_1_wrist.x < hand_2_wrist.x:
            return hand_landmarks_list[0], hand_landmarks_list[1]
        else:
            return hand_landmarks_list[1], hand_landmarks_list[0]

    def is_click_gesture_detected(self, hand_landmarks, w, h):
        thumb_tip = self.get_thumb_tip(hand_landmarks, w, h)  # Get thumb position
        index_tip = self.get_index_tip(hand_landmarks, w, h)  # Get index finger position

        distance = math.hypot(index_tip.x - thumb_tip.x, index_tip.y - thumb_tip.y)  # Distance between thumb and index finger

        # Detect the state of thumb and index finger touching
        click_gesture_detected = True if distance < self.CLICK_DIST_THRESHOLD else False
        if not self.click_gesture_history or click_gesture_detected != self.click_gesture_history[-1]:
            self.click_gesture_history.append(click_gesture_detected)

        return click_gesture_detected

    def get_thumb_tip(self, hand_landmarks, w, h) -> Position:
        return get_point(self.mp_hands.HandLandmark.THUMB_TIP, hand_landmarks, w, h)
    
    def get_index_tip(self, hand_landmarks, w, h) -> Position:
        return get_point(self.mp_hands.HandLandmark.INDEX_FINGER_TIP, hand_landmarks, w, h)

    def get_wrist(self, hand_landmarks, w, h) -> Position:
        return get_point(self.mp_hands.HandLandmark.WRIST, hand_landmarks, w, h)
    
    def get_cursor_position(self, w, h, hand_landmarks) -> Position:
        thumb_tip = self.get_thumb_tip(hand_landmarks, w, h)  # Get thumb position
        index_tip = self.get_index_tip(hand_landmarks, w, h)  # Get index finger position

        middle_point_x = (thumb_tip.x + index_tip.x) // 2
        middle_point_y = (thumb_tip.y + index_tip.y) // 2

        return Position(middle_point_x, middle_point_y)