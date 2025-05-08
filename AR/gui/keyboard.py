from .draw import *
from hand_detection_models import *


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

    def draw(self, 
             image: np.ndarray, 
             start_x: int, start_y: int, 
             gesture: DetectionModel, 
             color, border_color, font_color, 
             hover_color, hover_border_color, hover_font_color,
             key_size, padding,
             draw_blank_keys: bool = True):
        
        self.key_size = int(key_size)
        self.padding = int(padding)

        left_detected_key = self.detect_key_press(gesture.left_hand.cursor, start_x, start_y, draw_blank_keys)
        right_detected_key = self.detect_key_press(gesture.right_hand.cursor, start_x, start_y, draw_blank_keys)

        if gesture.left_hand.clicked or gesture.right_hand.clicked:
            detected_key = left_detected_key if gesture.left_hand.clicked else right_detected_key

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

        overlay = image.copy()

        # Procházení kláves a jejich vykreslení
        for row_idx, row in enumerate(self.keys):
            for col_idx, key in enumerate(row):
                if key == "" or key == " ":
                    if not draw_blank_keys:
                        continue
                    
                x1 = start_x + col_idx * (self.key_size + self.padding)
                y1 = start_y + row_idx * (self.key_size + self.padding)
                x2 = x1 + self.key_size
                y2 = y1 + self.key_size

                new_color = hover_color if right_detected_key == key or left_detected_key == key else color
                new_border_color = hover_border_color if right_detected_key == key or left_detected_key == key else border_color
                new_font_color = hover_font_color if right_detected_key == key or left_detected_key == key else font_color

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

    def detect_key_press(self, cursor: Position, start_x: int, start_y: int, draw_blank_keys: bool):
        x, y = cursor.get_array()

        if x is None or y is None:
            return None

        # Procházení kláves a kontrola, zda kliknutí spadá do jejich oblasti
        for row_idx, row in enumerate(self.keys):
            for col_idx, key in enumerate(row):
                x1 = start_x + col_idx * (self.key_size + self.padding)
                y1 = start_y + row_idx * (self.key_size + self.padding)
                x2 = x1 + self.key_size
                y2 = y1 + self.key_size

                if x1 <= x <= x2 and y1 <= y <= y2:
                    if not draw_blank_keys and (key == "" or key == " "):
                        return None
                    return key  # Vrátí stisknutou klávesu
        return None