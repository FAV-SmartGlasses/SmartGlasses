import cv2
from draw import *
from gui.design_manager import *

class Keyboard:
    def __init__(self, layout : list[list[str]], key_size = 50, padding = 10, text = ""):
        self.text = text
        self.click_history = []
        self.keys = layout
        self.key_size = key_size  # Velikost jedné klávesy (čtverec)
        self.padding = padding  # Mezera mezi klávesami
        self.detected_key = None

    def process_detected_key(self, detected_key):
        raise NotImplemented()

    def draw(self, image, w, h, click_gesture_detected, cursor_position, 
             color, border_color, font_color, hover_color, hover_border_color, hover_font_color):
        detected_key = self.detect_key_press(cursor_position[0], cursor_position[1], w, h)

        if click_gesture_detected:
            if detected_key is not None:
                if len(self.click_history) != 0:
                    if not self.click_history[-1]:
                        self.process_detected_key(detected_key)
                        print(f"Stisknuta klávesa: {detected_key}")
                        self.click_history.append(True)
                else:
                    self.click_history.append(True)
        else:
            if len(self.click_history) != 0 and self.click_history[-1]:
                self.click_history.append(False)

        # Výpočet počáteční pozice klávesnice
        start_x = w // 2 - (len(self.keys[0]) * (self.key_size + self.padding)) // 2
        start_y = h // 2 - (len(self.keys) * (self.key_size + self.padding)) // 2

        # Vytvoření překryvného obrázku
        overlay = image.copy()

        # Procházení kláves a jejich vykreslení
        for row_idx, row in enumerate(self.keys):
            for col_idx, key in enumerate(row):
                x1 = start_x + col_idx * (self.key_size + self.padding)
                y1 = start_y + row_idx * (self.key_size + self.padding)
                x2 = x1 + self.key_size
                y2 = y1 + self.key_size

                new_color = hover_color if detected_key == key else color
                new_border_color = hover_border_color if detected_key == key else border_color
                new_font_color = hover_font_color if detected_key == key else font_color

                # Vykreslení klávesy (obdélník)
                #cv2.rectangle(overlay, (x1, y1), (x2, y2), color, -1)
                #cv2.rectangle(overlay, (x1, y1), (x2, y2), BLACK, 2)

                draw_rounded_rectangle(overlay, 
                                        (x1, y1), 
                                        (x2, y2), 
                                        10, 
                                        new_color, 
                                        -1)
                
                draw_rounded_rectangle(overlay,
                                        (x1, y1), 
                                        (x2, y2), 
                                        10, 
                                        new_border_color, 
                                        2)

                # Vykreslení textu klávesy
                text_size = cv2.getTextSize(key, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
                text_x = x1 + (self.key_size - text_size[0]) // 2
                text_y = y1 + (self.key_size + text_size[1]) // 2
                cv2.putText(overlay, key, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, new_font_color, 2)

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