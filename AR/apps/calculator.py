import math

from apps.app_base import FixedAspectApp
from gui.draw import *
from gui.keyboard import Keyboard
from hand_detection_models import *
from other_utilities import *

MAX_LENGTH = 10

KEYS = [
    ["<-", "->", "^", "pi"],
    ["C", "()", "%", "/"],
    ["7", "8", "9", "*"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "X", "="]
]

class Calculator(FixedAspectApp):
    def __init__(self, name: str, display_name: str, icon_path: str):
        super().__init__(name, display_name, icon_path)

        self.keyboard = CalculatorKeyboard(KEYS)
        self.keyboard.set_colors(get_neutral_color_bgra(), get_neutral_color2_bgra(), get_font_color_bgra(), 
                                get_neutral_color2_bgra(), get_nice_color_bgra(), get_nice_color_bgra())

        self.aspect_ratio = self.compute_aspect_ratio()

        # Default size, will be dynamically updated
        self._size: Size = Size(300, int(300 / self.aspect_ratio))
        self._position: Position = Position(0, 0)

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

    def draw(self, image: np.ndarray, gestures: DetectionModel):
        """Draw the calculator UI dynamically based on the current size"""
        cv2.setUseOptimized(True)

        overlay = image.copy()

        if self.opened:
            self.check_fist_gesture(gestures)
            self.check_resize_gesture(gestures)

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
            draw_rounded_rectangle(
                overlay,
                self._position.get_array(),
                get_right_bottom_pos(self._position, self._size).get_array(),
                30,
                get_nice_color_bgra(),  # Use BGRA color
                -1)
            
            self.keyboard.set_position_and_size(
                                Position(self._position.x + scaled_padding, self._position.y + textbox_height + scaled_padding),
                                scaled_key_size,
                                scaled_key_padding)
            
            self.keyboard.draw(overlay, gestures)

            # Kombinace původního obrázku a překryvného obrázku s průhledností
            alpha = get_app_transparency()
            cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)

            # Draw the text inside the textbox
            text_size = cv2.getTextSize(self.keyboard._text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
            text_x = self._position.x + (textbox_width - text_size[0]) // 2
            text_y = self._position.y + (textbox_height + text_size[1] + scaled_padding) // 2
            cv2.putText(
                image,
                self.keyboard.get_text_with_cursor(),
                (text_x, text_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                get_font_color_bgra(),  # Use BGRA color
                2)


class CalculatorKeyboard(Keyboard):
    def __init__(self, layout: list[list[str]]):
        super().__init__(layout)
        self.evaluated = False
        self._text = "0"

    def process_detected_key(self, detected_key):
        if detected_key == "<-":
            if self._text and len(self._text) > self.cursor_in_text_position_from_back:
                self.cursor_in_text_position_from_back += 1
        elif detected_key == "->":
            if self._text and self.cursor_in_text_position_from_back > 0:
                self.cursor_in_text_position_from_back -= 1
        elif detected_key == "X":
            if self.evaluated:
                self._text = "0"
                self.evaluated = False
            if self._text:
                if len(self._text) > 0 and self.cursor_in_text_position_from_back < len(self._text):
                    cursor_position = len(self._text) - self.cursor_in_text_position_from_back
                    self._text = self._text[:cursor_position - 1] + self._text[cursor_position:] # deletes character on the place before cursor
                    #(cursor position from back stayes the same)
        elif detected_key == "C":
            self._text = "0"
            self.cursor_in_text_position_from_back = 0
        elif detected_key in "0123456789":
            if self.evaluated:
                self._text = ""
                self.cursor_in_text_position_from_back = 0
                self.evaluated = False
            if self._text == "0" or self._text == "":
                self._text = detected_key
            else:
                cursor_position = len(self._text) - self.cursor_in_text_position_from_back
                self._text = self._text[:cursor_position] + detected_key + self._text[cursor_position:]
        elif detected_key in "+-*/%^":
            cursor_position = len(self._text) - self.cursor_in_text_position_from_back
            # Add an operator if the last character is not an operator
            if self._text and self._text[cursor_position - 1] not in "+-*/%^":
                if self.evaluated:
                    self.cursor_in_text_position_from_back = 0
                    self.evaluated = False
                self._text = self._text[:cursor_position] + detected_key + self._text[cursor_position:]
        elif detected_key == "pi":
            cursor_position = len(self._text) - self.cursor_in_text_position_from_back
            if self.evaluated:
                self._text = ""
                self.cursor_in_text_position_from_back = 0
                self.evaluated = False
            self._text = self._text[:cursor_position] + detected_key + self._text[cursor_position:]
        elif detected_key == ".":
            cursor_position = len(self._text) - self.cursor_in_text_position_from_back

            # Přidání desetinné tečky pouze pokud:
            # 1. Před kurzorem je číslo (nebo text je prázdný a začínáme s "0.")
            # 2. V aktuálním čísle (od posledního operátoru nebo závorky) ještě není desetinná tečka
            if not self._text:
                self._text = "0."
            else:
                # Najdeme poslední operátor nebo závorku před kurzorem
                last_operator_pos = max(
                    self._text.rfind(op, 0, cursor_position) for op in "+-*/%()"
                )
                # Extrahujeme aktuální číslo
                current_number = self._text[last_operator_pos + 1:cursor_position]

                # Přidáme tečku, pokud aktuální číslo neobsahuje tečku
                if "." not in current_number:
                    self._text = self._text[:cursor_position] + "." + self._text[cursor_position:]
        elif detected_key == "()":
            cursor_position = len(self._text) - self.cursor_in_text_position_from_back

            # Add parentheses
            if not self._text or self._text[cursor_position-1] in "+-*/%(":
                self._text = self._text[:cursor_position] + "(" + self._text[cursor_position:]
            elif self._text[cursor_position - 1].isdigit() or self._text[cursor_position - 1] == ")":
                if self._text.count("(") > self._text.count(")"):
                    self._text = self._text[:cursor_position] + ")" + self._text[cursor_position:]
                else:
                    self._text = self._text[:cursor_position] + "(" + self._text[cursor_position:]
        elif detected_key == "=" and self._text:
            # Evaluate the expression
            try:
                self._text = self._text.replace("pi", str(math.pi))
                self._text = self._text.replace("^", "**")
                self._text = str(eval(self._text))
            except (SyntaxError, ZeroDivisionError):
                self._text = "Invalid"
            self.evaluated = True

        # Limit the text length
        self._text = self._text[:MAX_LENGTH]
        print(f"Current text: {self._text}")