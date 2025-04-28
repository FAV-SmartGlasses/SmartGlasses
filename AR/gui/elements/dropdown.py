import numpy as np

from gui.draw import *
from .element_base import Element
from other_utilities import Position, Size
from hand_detection_models import DetectionModel


class Dropdown(Element):
    def __init__(self, position: Position, size: Size, options: tuple[str], selected_option: int=None):
        super().__init__(position, size)
        self.open = False
        self.options = options
        self.selected_option = selected_option
        self.padding = 10
        self.click_history = []

    def draw(self, image: np.ndarray, gestures: DetectionModel): # TODO: teach Thomas how function overriding works
        
        is_left_hovered = is_cursor_in_rect(gestures.left_hand.cursor, (self._position.x, self._position.y, self._position.x + self._size.w, self._position.y + self._size.h))
        is_right_hovered = is_cursor_in_rect(gestures.right_hand.cursor, (self._position.x, self._position.y, self._position.x + self._size.w, self._position.y + self._size.h))
        is_left_clicked = is_left_hovered and gestures.left_hand.click_gesture_detected
        is_right_clicked = is_right_hovered and gestures.right_hand.click_gesture_detected
        is_clicked = is_left_clicked or is_right_clicked

        if is_clicked:
            if len(self.click_history) == 0 or (len(self.click_history) != 0 and self.click_history[-1] == False):
                self.open = not self.open
                self.click_history.append(True)
        else:
            if len(self.click_history) == 0 or (len(self.click_history) != 0 and self.click_history[-1]):
                self.click_history.append(False)
        

        text = self.selected_option if self.selected_option else "Select an option"
        self.draw_element(image, text)

        if self.open:
            for idx, option in enumerate(self.options):
                option_x = self._position.x
                option_y = self._position.y + (idx + 1) * (self._size.h + self.padding)

                # Zkontrolujeme, jestli je kurzor nad možností
                rect = (option_x, option_y, option_x + self._size.w, option_y + self._size.h)
                hovered = False

                option_left_hovered = is_cursor_in_rect(gestures.left_hand.cursor, rect)
                option_right_hovered = is_cursor_in_rect(gestures.right_hand.cursor, rect)
                if option_left_hovered or option_right_hovered:
                    hovered = True

                    if ((gestures.left_hand.click_gesture_detected and option_left_hovered) or 
                        (gestures.right_hand.click_gesture_detected and option_right_hovered)):
                        self.selected_option = option
                        self.open = False

                self.draw_option(image, option_x, option_y, hovered, option)
        
    def draw_element(self, image: np.ndarray, text: str):
        size_y = self._size.h * (len(self.options) + 1) + self.padding * (len(self.options) + 1) if self.open else self._size.h
        draw_rounded_rectangle(image, (self._position.x, self._position.y), (self._position.x + self._size.w, self._position.y + size_y), 15, get_nice_color(), -1)
        cv2.putText(image, text, (self._position.x + 10, self._position.y + 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, get_font_color(), 2)

    def draw_option(self, image: np.ndarray, x: int, y: int, hovered: bool, text: str):
        color = get_nice_color() if hovered else get_neutral_color()
        draw_rounded_rectangle(image, (x + self.padding, y), (x + self._size.w - self.padding, y + self._size.h), 15, color, -1)
        cv2.putText(image, text, (x + self.padding + 10, y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, get_font_color(), 2)