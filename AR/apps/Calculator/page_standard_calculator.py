import numpy as np

from apps.page_base import FixedAspectPage
from gui.draw import *
from gui.keyboard import Keyboard
from hand_detection_models import *
from other_utilities import *

MAX_LENGTH = 10

KEYS = [
    ["^", "()", "%", "/"],
    ["7", "8", "9", "*"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "X", "="]
]

class Standard(FixedAspectPage):
    def __init__(self):
        super().__init__()

        self.keyboard = CalculatorKeyboard(KEYS)
        self.keyboard.set_colors(get_neutral_color_bgra(), get_neutral_color2_bgra(), get_font_color_bgra(), 
                                get_neutral_color2_bgra(), get_nice_color_bgra(), get_nice_color_bgra())

        self.aspect_ratio = self.compute_aspect_ratio()

        # Default size, will be dynamically updated
        self._size = Size(800, int(800 / self.aspect_ratio))
        self._position = Position(0, 0)

    def compute_aspect_ratio(self):
        """Compute the aspect ratio based on the layout"""
        cols = len(KEYS[0])
        rows = len(KEYS)
        sample_key_size = 10  # libovolná jednotka, důležité jsou proporce
        sample_padding = sample_key_size // 2
        sample_key_padding = sample_padding // 2
        sample_textbox_height = sample_key_size

        total_width = cols * sample_key_size + (cols - 1) * sample_key_padding + 2 * sample_padding
        total_height = rows * sample_key_size + (rows - 1) * sample_key_padding + sample_textbox_height + 2 * sample_padding

        return total_width / total_height

    def draw(self, image_overlay: np.ndarray, gesture: DetectionModel):
        """Draw the calculator UI dynamically based on the current size"""
        cv2.setUseOptimized(True)

        cols = len(KEYS[0])
        rows = len(KEYS)
        sample_key_size = 10  # libovolná jednotka, důležité jsou proporce
        sample_padding = sample_key_size // 2
        sample_key_padding = sample_padding // 2
        sample_textbox_height = sample_key_size

        total_width = cols * sample_key_size + (cols - 1) * sample_key_padding + 2 * sample_padding

        ratio = self._size.w / total_width

        scaled_padding = int(sample_padding * ratio)
        scaled_key_size = int(sample_key_size * ratio)
        scaled_key_padding = int(sample_key_padding * ratio)
        textbox_height = int(sample_textbox_height * ratio)

        # Draw the textbox background
        textbox_width = self._size.w
        """draw_rounded_rectangle(
            image_overlay,
            self._position.get_array(),
            (self._position.x + textbox_width,
             self._position.y + self._size.h),
            30,
            get_nice_color_bgra(),  # Use BGRA color
            -1
        )"""

        # Draw the text inside the textbox
        text_size = cv2.getTextSize(self.keyboard.text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
        text_x = self._position.x + (textbox_width - text_size[0]) // 2
        text_y = self._position.y + (textbox_height + text_size[1] + scaled_padding) // 2
        cv2.putText(
            image_overlay,
            self.keyboard.text,
            (text_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            get_font_color_bgra(),  # Use BGRA color
            2
        )

        self.keyboard.set_position_and_size(
                            Position(self._position.x + scaled_padding, self._position.y + textbox_height + scaled_padding),
                            scaled_key_size,
                            scaled_key_padding)
        
        self.keyboard.draw(image_overlay, gesture)

class CalculatorKeyboard(Keyboard):
    def __init__(self, layout: list[list[str]]):
        super().__init__(layout)
        self.evaluated = False
        self.text = ""

    def process_detected_key(self, detected_key):
        if detected_key == "X":
            if self.evaluated:
                self.text = ""
                self.evaluated = False
            if self.text:
                self.text = self.text[:-1]
        elif detected_key in "0123456789":
            if self.evaluated:
                self.text = ""
                self.evaluated = False
            # Přidání čísla
            if self.text == "0":
                self.text = detected_key
            else:
                self.text += detected_key
        elif detected_key in "+-*/%^":
            # Add an operator if the last character is not an operator
            if self.text and self.text[-1] not in "+-*/%^":
                if self.evaluated:
                    self.evaluated = False
                self.text += "**" if detected_key == "^" else detected_key
        elif detected_key == ".":
            # Add a decimal point if valid
            if self.text and self.text[-1].isdigit() and "." not in self.text.split()[-1]:
                self.text += detected_key
            elif not self.text:
                self.text = "0."
        elif detected_key == "()":
            # Add parentheses
            if not self.text or self.text[-1] in "+-*/%(":
                self.text += "("
            elif self.text[-1].isdigit() or self.text[-1] == ")":
                if self.text.count("(") > self.text.count(")"):
                    self.text += ")"
                else:
                    self.text += "("
        elif detected_key == "=" and self.text:
            # Evaluate the expression
            try:
                self.text = str(eval(self.text))
            except (SyntaxError, ZeroDivisionError):
                self.text = "Invalid"
            self.evaluated = True

        # Limit the text length
        self.text = self.text[:MAX_LENGTH]
        print(f"Current text: {self.text}")