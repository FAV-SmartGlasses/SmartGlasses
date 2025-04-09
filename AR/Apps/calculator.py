from menu import App
import cv2
from draw import Draw

class Calculator(App):
    def __init__(self, name, display_name, icon_path):
        super().__init__(name, display_name, icon_path)
        self.text = ""
        self.click_history = []
        self.keys = [
            ["^", "()", "%", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ",", "X", "="]
        ]
        self.key_size = 50  # Velikost jedné klávesy (čtverec)
        self.padding = 10   # Mezera mezi klávesami

    def process_detected_key(self, detected_key):
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
        elif detected_key in "+-*/%":
            # Přidání znaménka, pokud poslední znak není znaménko
            if self.text and self.text[-1] not in "+-*/%(":
                self.text += detected_key
        elif detected_key == ",":
            # Přidání čárky, pokud poslední znak je číslo a čárka již není v aktuálním čísle
            if self.text and self.text[-1].isdigit():
                # Zkontroluje, zda aktuální číslo již obsahuje čárku
                last_number = self.text.split()[-1]
                if "," not in last_number:
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
        print(f"Aktuální text: {self.text}")

    def draw(self, image, w, h, click_gesture_detected, cursor_position):
        #TODO: devide this function to more functions
        #TODO: make rounded corners for keys
        #TODO: make this app calculate the result of the expression
        #TODO: make better design of text box
        #TODO: add sliders if expression is too long
        #TODO: add second text box for result

        if(self.opened):
            detected_key = self.detect_key_press(cursor_position[0], cursor_position[1], w, h)

            if click_gesture_detected:
                if detected_key is not None:
                    if len(self.click_history) != 0:
                        if self.click_history[-1] == False:
                            self.process_detected_key(detected_key)
                            print(f"Stisknuta klávesa: {detected_key}")
                            self.click_history.append(True)
                    else:
                        self.click_history.append(True)
            else:
                if (len(self.click_history) != 0 and self.click_history[-1] == True):
                    self.click_history.append(False)

            # Výpočet počáteční pozice klávesnice
            start_x = w // 2 - (len(self.keys[0]) * (self.key_size + self.padding)) // 2
            start_y = h // 2 - (len(self.keys) * (self.key_size + self.padding)) // 2

            # Vytvoření překryvného obrázku
            overlay = image.copy()

            textbox_height = 60

            draw = Draw()
            draw.draw_rounded_rectangle(overlay,
                                         (start_x - self.padding, start_y - textbox_height), 
                                         (start_x + len(self.keys[0]) * (self.key_size + self.padding), 
                                          start_y + len(self.keys) * (self.key_size + self.padding)), 
                                          30, 
                                          (0, 0, 0), 
                                          -1)
            
            cv2.putText(overlay, self.text, 
                        (start_x + 10, start_y - textbox_height + 20), 
                        cv2.FONT_HERSHEY_SIMPLEX, 
                        1, 
                        (255, 255, 255), 
                        2)

            """cv2.rectangle(overlay, 
                          (start_x - self.padding, start_y - 50), 
                          (start_x + len(self.keys[0]) * (self.key_size + self.padding), 
                           start_y + len(self.keys) * (self.key_size + self.padding)), 
                           (0, 0, 0), -1)"""
            


            # Procházení kláves a jejich vykreslení
            for row_idx, row in enumerate(self.keys):
                for col_idx, key in enumerate(row):
                    x1 = start_x + col_idx * (self.key_size + self.padding)
                    y1 = start_y + row_idx * (self.key_size + self.padding)
                    x2 = x1 + self.key_size
                    y2 = y1 + self.key_size

                    color = (248, 255, 145) if detected_key == key else (255, 255, 255)

                    # Vykreslení klávesy (obdélník)
                    cv2.rectangle(overlay, (x1, y1), (x2, y2), color, -1)
                    cv2.rectangle(overlay, (x1, y1), (x2, y2), (0, 0, 0), 2)

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
                                                (0, 0, 0), 
                                                2)"""

                    # Vykreslení textu klávesy
                    text_size = cv2.getTextSize(key, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
                    text_x = x1 + (self.key_size - text_size[0]) // 2
                    text_y = y1 + (self.key_size + text_size[1]) // 2
                    cv2.putText(overlay, key, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

            # Kombinace původního obrázku a překryvného obrázku s průhledností
            alpha = 0.5  # Nastavení průhlednosti (0.0 = zcela průhledné, 1.0 = zcela neprůhledné)
            cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)

    def detect_key_press(self, x, y, w, h):
        if x is None or y is None:
            return None

        # Výpočet počáteční pozice klávesnice
        start_x = w // 2 - (len(self.keys[0]) * (self.key_size + self.padding)) // 2
        start_y = h // 2 - (len(self.keys) * (self.key_size + self.padding)) // 2

        # Procházení kláves a kontrola, zda kliknutí spadá do jejich oblasti
        for row_idx, row in enumerate(self.keys):
            for col_idx, key in enumerate(row):
                x1 = start_x + col_idx * (self.key_size + self.padding)
                y1 = start_y + row_idx * (self.key_size + self.padding)
                x2 = x1 + self.key_size
                y2 = y1 + self.key_size

                if x1 <= x <= x2 and y1 <= y <= y2:
                    return key  # Vrátí stisknutou klávesu
        return None

            