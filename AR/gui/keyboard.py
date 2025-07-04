from hand_detection_models import *
from .draw import *


class Keyboard:
    def __init__(self, layout : list[list[str]], text = ""):
        self.text = text
        self.click_history = []
        self.keys: list[list[str]] = layout
        self.key_size: int
        self.key_padding: int
        self.detected_key = None
        self.position: Position | None = None
        self.cursor_in_text_position_from_back: int = 0 # 0 means cursor is at the end of the text

        self.key_size = 0
        self.key_padding = 0

        self.color = None
        self.border_color = None
        self.font_color = None
        self.hover_color = None
        self.hover_border_color = None
        self.hover_font_color = None

    def process_detected_key(self, detected_key):
        raise NotImplemented()
    
    def set_position_and_size(self, position: Position, key_size: int, padding: int):
        self.position = position
        self.key_size = key_size
        self.key_padding = padding

    def set_colors(self, color, border_color, font_color, hover_color, hover_border_color, hover_font_color):
        self.color = color
        self.border_color = border_color
        self.font_color = font_color
        self.hover_color = hover_color
        self.hover_border_color = hover_border_color
        self.hover_font_color = hover_font_color

    def get_text_with_cursor(self):
        """returns text with cursor as char |  on right place"""
        if self.cursor_in_text_position_from_back <= len(self.text):
            cursor_position = len(self.text) - self.cursor_in_text_position_from_back
            return self.text[:cursor_position] + "|" + self.text[cursor_position:]
        else:
            self.cursor_in_text_position_from_back = 0
            return self.text + "|"

    def draw(self, image: np.ndarray, gesture: DetectionModel, draw_blank_keys: bool = True):
        left_detected_key = self.detect_key_press(gesture.left_hand.cursor, draw_blank_keys)
        right_detected_key = self.detect_key_press(gesture.right_hand.cursor, draw_blank_keys)

        if gesture.left_hand.clicked or gesture.right_hand.clicked:
            detected_key = left_detected_key if gesture.left_hand.clicked else right_detected_key

            if detected_key is not None:
                if len(self.click_history) != 0:
                    if not self.click_history[-1]:
                        self.process_detected_key(detected_key)
                        self.click_history.append(True)
                else:
                    self.click_history.append(True)
        else:
            if len(self.click_history) != 0 and self.click_history[-1]:
                self.click_history.append(False)

        overlay = image.copy()

        for row_idx, row in enumerate(self.keys):
            for col_idx, key in enumerate(row):
                if key == "" or key == " ":
                    if not draw_blank_keys:
                        continue

                x1 = self.position.x + col_idx * (self.key_size + self.key_padding)
                y1 = self.position.y + row_idx * (self.key_size + self.key_padding)
                x2 = x1 + self.key_size
                y2 = y1 + self.key_size

                new_color = self.hover_color if right_detected_key == key or left_detected_key == key else self.color
                new_border_color = self.hover_border_color if right_detected_key == key or left_detected_key == key else self.border_color
                new_font_color = self.hover_font_color if right_detected_key == key or left_detected_key == key else self.font_color

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

                text_size = cv2.getTextSize(key, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
                text_x = x1 + (self.key_size - text_size[0]) // 2
                text_y = y1 + (self.key_size + text_size[1]) // 2
                cv2.putText(overlay, key, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, new_font_color, 2)

        alpha = 0.5
        cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)

    def detect_key_press(self, cursor: Position, draw_blank_keys: bool):
        if cursor.x is None or cursor.y is None:
            return None

        for row_idx, row in enumerate(self.keys):
            for col_idx, key in enumerate(row):
                x1 = self.position.x + col_idx * (self.key_size + self.key_padding)
                y1 = self.position.y + row_idx * (self.key_size + self.key_padding)
                x2 = x1 + self.key_size
                y2 = y1 + self.key_size

                if x1 <= cursor.x <= x2 and y1 <= cursor.y <= y2:
                    if not draw_blank_keys and (key == "" or key == " "):
                        return None
                    return key
        return None