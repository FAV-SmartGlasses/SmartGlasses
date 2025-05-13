import mediapipe as mp
import cv2
import math
import numpy as np
from collections import deque
from enum import Enum

from config import *
from other_utilities import Position
from hand_detection_models import *

class HandDetection:
    DIST_THRESHOLD = 40  # finger touch threshold

    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7)
        self.click_gesture_history = deque(maxlen=20)  # save the last states
        self.last_left_wrist: Position = Position()
        self.last_right_wrist: Position = Position()

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

        result = DetectionModel()
        left_swipe_gesture_detected = SwipeGesture.NO
        right_swipe_gesture_detected = SwipeGesture.NO

        hand_landmarks_list = hands_results.multi_hand_landmarks
        if hand_landmarks_list:                    
            if len(hand_landmarks_list) == 2:
                # TODO: add gesture for moving and resizing apps

                left_hand, right_hand = self.get_left_and_right_hands(hand_landmarks_list, w, h)

                result.left_hand.fist = self.is_fist_detected(left_hand)
                result.right_hand.fist = self.is_fist_detected(right_hand)
                print(f"left fist: {result.left_hand.fist}, right fist: {result.right_hand.fist}")
                if result.right_hand.fist and result.left_hand.fist:
                    cv2.putText(image, "both fists!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                elif result.left_hand.fist:
                    cv2.putText(image, "left fist!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                elif result.right_hand.fist:
                    cv2.putText(image, "right fist!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                left_swipe_gesture_detected = self.swipe_gesture_detected(left_hand, w, h, is_left = True)
                right_swipe_gesture_detected = self.swipe_gesture_detected(right_hand, w, h, is_left = False)

                result.left_hand.clicked = self.is_click_gesture_detected(left_hand, w, h)
                result.right_hand.clicked = self.is_click_gesture_detected(right_hand, w, h)

                result.left_hand.cursor = self.get_cursor_position(w, h, left_hand)
                result.right_hand.cursor = self.get_cursor_position(w, h, right_hand)

                self.draw(image, left_hand)
                self.draw(image, right_hand)
            elif len(hand_landmarks_list) == 1:
                hand_landmarks = hand_landmarks_list[0]

                result.right_hand.fist = self.is_fist_detected(hand_landmarks)
                print(f"fist: {result.right_hand.fist}")
                if result.right_hand.fist:
                    cv2.putText(image, "fist!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                right_swipe_gesture_detected = self.swipe_gesture_detected(hand_landmarks, w, h, is_left=False)
                result.right_hand.clicked = self.is_click_gesture_detected(hand_landmarks, w, h)
                result.right_hand.cursor = self.get_cursor_position(w, h, hand_landmarks)
                result.left_hand.cursor = Position()
                self.draw(image, hand_landmarks)
            elif len(hand_landmarks_list) == 0:
                result.right_hand.cursor = Position()
                result.left_hand.cursor = Position()

        if result.left_hand.clicked and result.right_hand.clicked:
            result.left_hand.clicked = False
            result.right_hand.clicked = False

        result.swipe = self.combine_swipe_gestures(left_swipe_gesture_detected, right_swipe_gesture_detected)

        if PRINT_SWIPE_GESTURES and result.swipe is not SwipeGesture.NO:
            print(result.swipe.name)

        return image, result

#region fist detection
    def calculate_distance_3d(self, point1, point2):
        return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2 + (point1.z - point2.z) ** 2)
    
    def is_fist_detected(self, hand_landmarks) -> bool:
        #getting positions of every finger
        thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
        index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        middle_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        ring_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP]
        pinky_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_TIP]

        # calculating distances between fingers with 3D coordinates
        thumb_index_distance = self.calculate_distance_3d(thumb_tip, index_tip)
        index_middle_distance = self.calculate_distance_3d(index_tip, middle_tip)
        middle_ring_distance = self.calculate_distance_3d(middle_tip, ring_tip)
        ring_pinky_distance = self.calculate_distance_3d(ring_tip, pinky_tip)

        # if distances between fingers are smaller than DISTANCE_TREESHOLD, fist gesture is detected
        DISTANCE_TREESHOLD = 0.05
        return (thumb_index_distance < DISTANCE_TREESHOLD and index_middle_distance < DISTANCE_TREESHOLD and 
                middle_ring_distance < DISTANCE_TREESHOLD and ring_pinky_distance < DISTANCE_TREESHOLD)
#endregion

#region swipe gesture
    def swipe_gesture_detected(self, hand_landmarks, w, h, is_left):
        wrist = self.get_wrist(hand_landmarks, w, h)  # Get wrist position

        if is_left:
            last_wrist_x = self.last_left_wrist.x
            last_wrist_y = self.last_left_wrist.y
        else:
            last_wrist_x = self.last_right_wrist.x
            last_wrist_y = self.last_right_wrist.y

        if last_wrist_x is not None and last_wrist_y is not None:
            delta_x = wrist.x - last_wrist_x
            delta_y = wrist.y - last_wrist_y
            threshold = 50

            if abs(delta_x) > abs(delta_y):  # Horizontal movement
                if delta_x > threshold:
                    gesture_detected = SwipeGesture.RIGHT
                    print(f"{'Left' if is_left else 'Right'} hand swipe right")
                elif delta_x < -threshold:
                    gesture_detected = SwipeGesture.LEFT
                    print(f"{'Left' if is_left else 'Right'} hand swipe left")
                else:
                    gesture_detected = SwipeGesture.NO
            else:  # Vertical movement
                if delta_y > threshold:
                    gesture_detected = SwipeGesture.DOWN
                    print(f"{'Left' if is_left else 'Right'} hand swipe down")
                elif delta_y < -threshold:
                    gesture_detected = SwipeGesture.UP
                    print(f"{'Left' if is_left else 'Right'} hand swipe up")
                else:
                    gesture_detected = SwipeGesture.NO
        else:
            gesture_detected = SwipeGesture.NO

        # Save the last wrist position
        if is_left:
            self.last_left_wrist = wrist
        else:
            self.last_right_wrist = wrist

        return gesture_detected

    def combine_swipe_gestures(self, left_gesture: SwipeGesture, right_gesture: SwipeGesture):
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
#endregion

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
        click_gesture_detected = True if distance < self.DIST_THRESHOLD else False
        if not self.click_gesture_history or click_gesture_detected != self.click_gesture_history[-1]:
            self.click_gesture_history.append(click_gesture_detected)

        return click_gesture_detected

#region get points
    def get_point(self, id_, hand_landmarks, w, h) -> Position:
        lm = hand_landmarks.landmark[id_]
        return Position(int(lm.x * w), int(lm.y * h))

    def get_thumb_tip(self, hand_landmarks, w, h) -> Position:
        return self.get_point(self.mp_hands.HandLandmark.THUMB_TIP, hand_landmarks, w, h)
    
    def get_index_tip(self, hand_landmarks, w, h) -> Position:
        return self.get_point(self.mp_hands.HandLandmark.INDEX_FINGER_TIP, hand_landmarks, w, h)

    def get_wrist(self, hand_landmarks, w, h) -> Position:
        return self.get_point(self.mp_hands.HandLandmark.WRIST, hand_landmarks, w, h)
    
    def get_cursor_position(self, w, h, hand_landmarks) -> Position:
        thumb_tip = self.get_thumb_tip(hand_landmarks, w, h)  # Get thumb position
        index_tip = self.get_index_tip(hand_landmarks, w, h)  # Get index finger position

        middle_point_x = (thumb_tip.x + index_tip.x) // 2
        middle_point_y = (thumb_tip.y + index_tip.y) // 2

        return Position(middle_point_x, middle_point_y)
#endregion