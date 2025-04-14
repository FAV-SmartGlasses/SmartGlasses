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
        self.hands = self.mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.7)
        self.click_gesture_history = deque(maxlen=20)  # save the last states
        self.last_left_wrist_x = None
        self.last_left_wrist_y = None
        self.last_right_wrist_x = None
        self.last_right_wrist_y = None

    def process_image(self, image, w, h):
        results = self.hands.process(image)

        left_click_gesture_detected = False
        right_click_gesture_detected = False
        left_swipe_gesture_detected = self.SwipeGesture.NO
        right_swipe_gesture_detected = self.SwipeGesture.NO
        left_cursor_position = None, None
        right_cursor_position = None, None

        if results.multi_hand_landmarks:
            hand_landmarks_list = results.multi_hand_landmarks
            if len(hand_landmarks_list) == 2:
                # TODO: add gesture for moving and resizing apps

                left_hand, right_hand = self.get_left_and_right_hands(hand_landmarks_list, w, h)

                left_swipe_gesture_detected = self.swipe_gesture_detected(left_hand, w, h, is_left=True)
                right_swipe_gesture_detected = self.swipe_gesture_detected(right_hand, w, h, is_left=False)

                left_click_gesture_detected = self.is_click_gesture_detected(left_hand, w, h)
                right_click_gesture_detected = self.is_click_gesture_detected(right_hand, w, h)

                left_cursor_position = self.get_cursor_position(w, h, left_hand)
                right_cursor_position = self.get_cursor_position(w, h, right_hand)

                self.draw(w, h, image, left_hand)
                self.draw(w, h, image, right_hand)
            elif len(hand_landmarks_list) == 1:
                hand_landmarks = hand_landmarks_list[0]
                right_swipe_gesture_detected = self.swipe_gesture_detected(hand_landmarks, w, h, is_left=True)
                right_click_gesture_detected = self.is_click_gesture_detected(hand_landmarks, w, h)
                right_cursor_position = self.get_cursor_position(w, h, hand_landmarks)
                self.draw(w, h, image, hand_landmarks)

        if left_click_gesture_detected and right_click_gesture_detected:
            left_click_gesture_detected = False
            right_click_gesture_detected = False

        swipe_gesture_detected = self.combine_swipe_gestures(left_swipe_gesture_detected, right_swipe_gesture_detected)

        return (image, left_click_gesture_detected, right_click_gesture_detected,
                swipe_gesture_detected, left_cursor_position, right_cursor_position)

    class SwipeGesture(Enum):
        NO = 0
        RIGHT = 1
        LEFT = 2
        DOWN = 3
        UP = 4
        BOTH_RIGHT = 5
        BOTH_LEFT = 6
        BOTH_OUT = 7
        BOTH_IN = 8

    def swipe_gesture_detected(self, hand_landmarks, w, h, is_left):
        wrist = self.get_wrist(hand_landmarks, w, h)  # Get wrist position

        if is_left:
            last_wrist_x = self.last_left_wrist_x
            last_wrist_y = self.last_left_wrist_y
        else:
            last_wrist_x = self.last_right_wrist_x
            last_wrist_y = self.last_right_wrist_y

        if last_wrist_x is not None and last_wrist_y is not None:
            delta_x = wrist[0] - last_wrist_x
            delta_y = wrist[1] - last_wrist_y
            threshold = 50

            if abs(delta_x) > abs(delta_y):  # Horizontal movement
                if delta_x > threshold:
                    gesture_detected = self.SwipeGesture.RIGHT
                    print(f"{'Left' if is_left else 'Right'} hand swipe right")
                elif delta_x < -threshold:
                    gesture_detected = self.SwipeGesture.LEFT
                    print(f"{'Left' if is_left else 'Right'} hand swipe left")
                else:
                    gesture_detected = self.SwipeGesture.NO
            else:  # Vertical movement
                if delta_y > threshold:
                    gesture_detected = self.SwipeGesture.DOWN
                    print(f"{'Left' if is_left else 'Right'} hand swipe down")
                elif delta_y < -threshold:
                    gesture_detected = self.SwipeGesture.UP
                    print(f"{'Left' if is_left else 'Right'} hand swipe up")
                else:
                    gesture_detected = self.SwipeGesture.NO
        else:
            gesture_detected = self.SwipeGesture.NO

        # Save the last wrist position
        if is_left:
            self.last_left_wrist_x = wrist[0]
            self.last_left_wrist_y = wrist[1]
        else:
            self.last_right_wrist_x = wrist[0]
            self.last_right_wrist_y = wrist[1]

        return gesture_detected

    def combine_swipe_gestures(self, left_gesture, right_gesture):
        if left_gesture == self.SwipeGesture.RIGHT and right_gesture == self.SwipeGesture.RIGHT:
            return self.SwipeGesture.BOTH_RIGHT
        elif left_gesture == self.SwipeGesture.LEFT and right_gesture == self.SwipeGesture.LEFT:
            return self.SwipeGesture.BOTH_LEFT
        elif left_gesture == self.SwipeGesture.LEFT and right_gesture == self.SwipeGesture.RIGHT:
            return self.SwipeGesture.BOTH_OUT
        elif left_gesture == self.SwipeGesture.RIGHT and right_gesture == self.SwipeGesture.LEFT:
            return self.SwipeGesture.BOTH_IN
        elif left_gesture != self.SwipeGesture.NO and right_gesture == self.SwipeGesture.NO:
            return left_gesture
        elif left_gesture == self.SwipeGesture.NO and right_gesture != self.SwipeGesture.NO:
            return right_gesture
        else:
            return self.SwipeGesture.NO

    def get_left_and_right_hands(self, hand_landmarks_list, w, h):
        hand_1_wrist = self.get_wrist(hand_landmarks_list[0], w, h)
        hand_2_wrist = self.get_wrist(hand_landmarks_list[1], w, h)

        if hand_1_wrist[0] < hand_2_wrist[0]:
            return hand_landmarks_list[0], hand_landmarks_list[1]
        else:
            return hand_landmarks_list[1], hand_landmarks_list[0]

    def is_click_gesture_detected(self, hand_landmarks, w, h):
        thumb_tip = self.get_thumb_tip(hand_landmarks, w, h)  # Get thumb position
        index_tip = self.get_index_tip(hand_landmarks, w, h)  # Get index finger position

        distance = math.hypot(index_tip[0] - thumb_tip[0], index_tip[1] - thumb_tip[1])  # Distance between thumb and index finger

        # Detect the state of thumb and index finger touching
        click_gesture_detected = True if distance < self.DIST_THRESHOLD else False
        if not self.click_gesture_history or click_gesture_detected != self.click_gesture_history[-1]:
            self.click_gesture_history.append(click_gesture_detected)

        return click_gesture_detected

    def get_point(self, id_, hand_landmarks, w, h):
        lm = hand_landmarks.landmark[id_]
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
    
    def get_cursor_position(self, w, h, hand_landmarks):
        thumb_tip = self.get_thumb_tip(hand_landmarks, w, h)  # Get thumb position
        index_tip = self.get_index_tip(hand_landmarks, w, h)  # Get index finger position

        middle_point_x = (thumb_tip[0] + index_tip[0]) // 2
        middle_point_y = (thumb_tip[1] + index_tip[1]) // 2

        return middle_point_x, middle_point_y

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