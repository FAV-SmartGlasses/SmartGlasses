import numpy as np
from apps.page_base import CalculatorPage
from gui.draw import *
from gui.keyboard import Keyboard

MAX_LENGTH = 10

KEYS = [
            ["^", "()", "%", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "X", "="]
        ]

PADDING = 10
KEY_SIZE = 50

class Standard(CalculatorPage):
    def __init__(self):
        self.keyboard = CalculatorKeyboard(KEYS)

    def draw(self, w, h,
             left_click_gesture_detected, right_click_gesture_detected, 
             left_cursor_position, right_cursor_position):
        # Create an overlay with transparency (BGRA)
        overlay = np.zeros((h, w, 4), dtype=np.uint8)

        # Calculate starting position for the keyboard
        start_x = w // 2 - (len(KEYS[0]) * (KEY_SIZE + PADDING)) // 2
        start_y = h // 2 - (len(KEYS) * (KEY_SIZE + PADDING)) // 2

        # Draw the textbox background
        textbox_height = 60
        draw_rounded_rectangle(overlay,
                                (start_x - PADDING, start_y - textbox_height), 
                                (start_x + len(KEYS[0]) * (KEY_SIZE + PADDING),
                                start_y + len(KEYS) * (KEY_SIZE + PADDING)),
                                30, 
                                get_nice_color_bgra(),  # Use BGRA color
                                -1)

        # Draw the text inside the textbox
        text_size = cv2.getTextSize(self.keyboard.text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
        text_x = start_x + (len(KEYS[0]) * (KEY_SIZE + PADDING) - text_size[0]) // 2
        text_y = start_y - textbox_height // 2 + text_size[1] // 2
        cv2.putText(overlay, self.keyboard.text, 
                    (text_x, text_y), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    1, 
                    get_font_color_bgra(),  # Use BGRA color
                    2)

        # Draw the keyboard
        self.keyboard.draw(overlay, w, h, 
                           left_click_gesture_detected, right_click_gesture_detected, 
                           left_cursor_position, right_cursor_position,
                           get_neutral_color_bgra(), get_neutral_color2_bgra(), get_font_color_bgra(), 
                           get_neutral_color2_bgra(), get_nice_color_bgra(), get_nice_color_bgra())

        return overlay
    
    

    def dynamic_draw(self, w, h, overlay,
                    left_click_gesture_detected, right_click_gesture_detected, 
                    left_cursor_position, right_cursor_position):
        
        # Dynamic scaling factor based on screen dimensions
        scale_factor = min(w, h) / 800  # Base size is 800px (could be adjusted)
        scaled_key_size = int(KEY_SIZE * scale_factor)  # Scale the key size
        scaled_padding = int(PADDING * scale_factor)  # Scale padding between keys

        # Create an overlay with transparency (BGRA)
        #overlay = np.zeros((h, w, 4), dtype=np.uint8)

        # Calculate starting position for the keyboard
        start_x = w // 2 - (len(KEYS[0]) * (scaled_key_size + scaled_padding)) // 2
        start_y = h // 2 - (len(KEYS) * (scaled_key_size + scaled_padding)) // 2

        # Draw the textbox background
        textbox_height = int(60 * scale_factor)  # Scale textbox height
        draw_rounded_rectangle(overlay,
                                (start_x - scaled_padding, start_y - textbox_height), 
                                (start_x + len(KEYS[0]) * (scaled_key_size + scaled_padding),
                                 start_y + len(KEYS) * (scaled_key_size + scaled_padding)),
                                30, 
                                get_nice_color_bgra(),  # Use BGRA color
                                -1)

        # Draw the text inside the textbox with dynamic text size
        text_size = cv2.getTextSize(self.keyboard.text, cv2.FONT_HERSHEY_SIMPLEX, scale_factor, 2)[0]
        text_x = start_x + (len(KEYS[0]) * (scaled_key_size + scaled_padding) - text_size[0]) // 2
        text_y = start_y - textbox_height // 2 + text_size[1] // 2
        cv2.putText(overlay, self.keyboard.text, 
                    (text_x, text_y), 
                    cv2.FONT_HERSHEY_SIMPLEX, 
                    scale_factor,  # Adjust font size dynamically
                    get_font_color_bgra(),  # Use BGRA color
                    2)

        # Draw the keyboard with dynamically scaled keys
        self.keyboard.draw(overlay, w, h, 
                           left_click_gesture_detected, right_click_gesture_detected, 
                           left_cursor_position, right_cursor_position,
                           get_neutral_color_bgra(), get_neutral_color2_bgra(), get_font_color_bgra(), 
                           get_neutral_color2_bgra(), get_nice_color_bgra(), get_nice_color_bgra(), 
                           scaled_key_size, scaled_padding)

        #return overlay

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