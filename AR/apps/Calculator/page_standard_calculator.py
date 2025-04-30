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

PADDING = 20
KEY_PADDING = PADDING/2
KEY_SIZE = 50

class Standard(FixedAspectPage):
    def __init__(self):
        super().__init__()

        self.keyboard = CalculatorKeyboard(KEYS)

        self.aspect_ratio = self.compute_aspect_ratio()

        self._size = Size(800, int(800 / self.aspect_ratio))
        self._position = Position(0, 0)

    def compute_aspect_ratio(self):
        cols = len(KEYS[0])
        rows = len(KEYS)
        sample_key_size = 10  # libovolná jednotka, důležité jsou proporce
        padding = sample_key_size // 5
        key_padding = padding/2
        textbox_height = sample_key_size

        total_width = cols * sample_key_size + (cols - 1) * key_padding + 2 * padding
        total_height = rows * sample_key_size + (rows - 1) * key_padding + textbox_height + padding

        return total_width / total_height

    def draw(self, image_overlay: np.ndarray, gesture: DetectionModel):
        
        cv2.setUseOptimized(True)
        
        # Dynamic scaling factor based on screen dimensions
        scale_factor = min(*self._size.get_array()) / 800  # Base size is 800px (could be adjusted)
        scaled_key_size = int(KEY_SIZE * scale_factor)  # Scale the key size
        scaled_padding = int(PADDING * scale_factor)  # Scale padding between keys
        scaled_key_padding = int(scaled_padding / 2)

        # Draw the textbox background
        textbox_height = int(60 * scale_factor)  # Scale textbox height
        draw_rounded_rectangle(image_overlay,
                                (self._position.x, self._position.y), 
                                (self._position.x + len(KEYS[0]) * (scaled_key_size + scaled_key_padding) - scaled_key_padding + 2 * scaled_padding,
                                 self._position.y + textbox_height + len(KEYS) * (scaled_key_size + scaled_key_padding) - scaled_key_padding + scaled_padding),
                                30, 
                                get_nice_color_bgra(),  # Use BGRA color
                                -1)

        # Draw the text inside the textbox with dynamic text size
        text_size = cv2.getTextSize(self.keyboard.text, cv2.FONT_HERSHEY_SIMPLEX, scale_factor, 2)[0]
        text_x = self._position.x + scaled_padding + (len(KEYS[0]) * (scaled_key_size + scaled_key_padding) - scaled_key_padding - text_size[0]) // 2
        text_y = self._position.y + (textbox_height - text_size[1]) // 2
        cv2.putText(image_overlay, self.keyboard.text, 
                    (text_x, text_y), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    scale_factor,  # Adjust font size dynamically
                    get_font_color_bgra(),  # Use BGRA color
                    2)

        # Draw the keyboard with dynamically scaled keys
        self.keyboard.draw(image_overlay, 
                           self._position.x + scaled_padding, 
                           self._position.y + textbox_height, gesture,
                           get_neutral_color_bgra(), get_neutral_color2_bgra(), get_font_color_bgra(), 
                           get_neutral_color2_bgra(), get_nice_color_bgra(), get_nice_color_bgra(), 
                           scaled_key_size,
                           scaled_key_padding)

class CalculatorKeyboard(Keyboard):
    def __init__(self, layout: list[list[str]]):
        super().__init__(layout)
        self.evaluated = False
        self.text = ""

    def process_detected_key(self, detected_key):
        if self.evaluated:
            self.text = ""
            self.evaluated = False

        if detected_key == "X":
            # Smazání posledního znaku
            if self.text:
                self.text = self.text[:-1]
        elif detected_key in "0123456789":
            # Přidání čísla
            if self.text == "0":
                # Pokud text obsahuje pouze "0", nahradí se novým číslem
                self.text = detected_key
            else:
                self.text += detected_key
        elif detected_key in "+-*/%^":
            # Přidání znaménka, pokud poslední znak není znaménko
            if self.text and self.text[-1] not in "+-*/%(^":
                if detected_key == "^":
                    self.text += "**"
                else:
                    self.text += detected_key
        elif detected_key == ".":
            # Přidání čárky, pokud poslední znak je číslo a čárka již není v aktuálním čísle
            if self.text and self.text[-1].isdigit():
                # Zkontroluje, zda aktuální číslo již obsahuje čárku
                last_number = self.text.split()[-1]
                if "." not in last_number:
                    self.text += detected_key
        elif detected_key == "()":
            # Přidání závorek s podporou vnořených závorek
            if not self.text or self.text[-1] in "+-*/%(":
                # Pokud je text prázdný nebo poslední znak je operátor/otevírací závorka, přidá se "("
                self.text += "("
            elif self.text[-1].isdigit() or self.text[-1] == ")":
                # Pokud poslední znak je číslo nebo zavírací závorka, přidá se ")"
                open_count = self.text.count("(")
                close_count = self.text.count(")")
                if open_count > close_count:
                    self.text += ")"
            else:
                # Jinak přidá otevírací závorku
                self.text += "("

        elif detected_key == "=" and len(self.text) > 0:
            try:
                self.text = str(eval(self.text))
            except SyntaxError or ZeroDivisionError:
                self.text = "Invalid"

            self.evaluated = True

        self.text = self.text[:MAX_LENGTH]

        print(f"Aktuální text: {self.text}")