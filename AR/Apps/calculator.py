from menu_items import App
import cv2
from gui.keyboard import Keyboard
from draw import draw_rounded_rectangle
from gui.design_manager import *

KEYS = [
            ["^", "()", "%", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "X", "="]
        ]

PADDING = 10
KEY_SIZE = 50

MAX_LENGTH = 10

class Calculator(App):
    def __init__(self, name, display_name, icon_path):
        super().__init__(name, display_name, icon_path)
        
        self.keyboard = CalculatorKeyboard(KEYS)

    def draw(self, image, w, h, click_gesture_detected, cursor_position):
        #TODO: make rounded corners for keys
        #TODO: make better design of text box

        if self.opened:
            self.keyboard.draw(image, w, h, click_gesture_detected, cursor_position)
            # Výpočet počáteční pozice klávesnice
            start_x = w // 2 - (len(KEYS[0]) * (KEY_SIZE + PADDING)) // 2
            start_y = h // 2 - (len(KEYS) * (KEY_SIZE + PADDING)) // 2

            # Vytvoření překryvného obrázku
            overlay = image.copy()

            textbox_height = 60

            draw_rounded_rectangle(overlay,
                                         (start_x - PADDING, start_y - textbox_height), 
                                         (start_x + len(KEYS[0]) * (KEY_SIZE + PADDING),
                                          start_y + len(KEYS) * (KEY_SIZE + PADDING)),
                                          30, 
                                          BLACK, 
                                          -1)
            
            cv2.putText(overlay, self.keyboard.text, 
                        (start_x + 10, start_y - textbox_height + 20), 
                        cv2.FONT_HERSHEY_SIMPLEX, 
                        1, 
                        WHITE,
                        2)

            """cv2.rectangle(overlay, 
                          (start_x - PADDING, start_y - 50), 
                          (start_x + len(self.keys[0]) * (KEY_SIZE + PADDING), 
                           start_y + len(self.keys) * (KEY_SIZE + PADDING)), 
                           BLACK, -1)"""

            # Procházení kláves a jejich vykreslení
            for row_idx, row in enumerate(KEYS):
                for col_idx, key in enumerate(row):
                    x1 = start_x + col_idx * (KEY_SIZE + PADDING)
                    y1 = start_y + row_idx * (KEY_SIZE + PADDING)
                    x2 = x1 + KEY_SIZE
                    y2 = y1 + KEY_SIZE

                    color = LIGHT_BLUE if self.keyboard.detected_key == key else WHITE

                    # Vykreslení klávesy (obdélník)
                    cv2.rectangle(overlay, (x1, y1), (x2, y2), color, -1)
                    cv2.rectangle(overlay, (x1, y1), (x2, y2), BLACK, 2)

                    """draw.draw_rounded_rectangle(overlay, 
                                                (x1, y1), 
                                                (x2, y2), 
                                                2, 
                                                color, 
                                                -1)
                    
                    draw.draw_rounded_rectangle(overlay, 
                                                (x1, y1), 
                                                (x2, y2), 
                                                2, 
                                                BLACK, 
                                                2)"""

                    # Vykreslení textu klávesy
                    text_size = cv2.getTextSize(key, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
                    text_x = x1 + (KEY_SIZE - text_size[0]) // 2
                    text_y = y1 + (KEY_SIZE + text_size[1]) // 2
                    cv2.putText(overlay, key, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, BLACK, 2)

            # Kombinace původního obrázku a překryvného obrázku s průhledností
            alpha = 0.5  # Nastavení průhlednosti (0.0 = zcela průhledné, 1.0 = zcela neprůhledné)
            cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)

class CalculatorKeyboard(Keyboard):
    def __init__(self, layout: list[list[str]]):
        super().__init__(layout)
        self.evaluated = False

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

        elif detected_key == "=":
            try:
                self.text = str(eval(self.text))
            except SyntaxError:
                self.text = "Invalid syntax"

            self.evaluated = True

        self.text = self.text[:MAX_LENGTH]

        print(f"Aktuální text: {self.text}")