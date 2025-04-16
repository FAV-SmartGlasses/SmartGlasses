from gui.draw import *
from gui.keyboard import Keyboard
from app_base import App

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
        self.btns = []
        #self.btns += Button(None, 200, 100, "Calculate", (100, 100),
                            #WHITE, BLACK, BLACK, LIGHT_BLUE, LIGHT_BLUE, BLACK)

    def draw(self, image, w, h, 
             left_click_gesture_detected, right_click_gesture_detected, 
             left_cursor_position, right_cursor_position):
        #TODO: make better design of text box

        if self.opened:
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
                                    get_nice_color(), 
                                    -1)
            
            text_size = cv2.getTextSize(self.keyboard.text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
            text_x = start_x + (len(KEYS[0]) * (KEY_SIZE + PADDING) - text_size[0]) // 2
            text_y = start_y - textbox_height // 2 + text_size[1] // 2
            cv2.putText(overlay, self.keyboard.text, 
                        (text_x, text_y), 
                        cv2.FONT_HERSHEY_SIMPLEX, 
                        1, 
                        get_font_color(),
                        2)
            
            # Kombinace původního obrázku a překryvného obrázku s průhledností
            alpha = 0.5  # Nastavení průhlednosti (0.0 = zcela průhledné, 1.0 = zcela neprůhledné)
            cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)
            
            overlay = image.copy()
            self.keyboard.draw(overlay, w, h, 
                                left_click_gesture_detected, right_click_gesture_detected, 
                                left_cursor_position, right_cursor_position,
                                get_neutral_color(), get_neutral_color2(), get_font_color(), 
                                get_neutral_color2(), get_nice_color(), get_nice_color())
                                            # WHITE, BLACK, BLACK, 
                                            # BLACK, LIGHT_BLUE, LIGHT_BLUE
            alpha = 0.5
            cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)

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