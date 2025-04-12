import cv2
from draw import *

class ToggleBtn:
    def __init__(self, x, y, height, text):
        self.x = x
        self.y = y
        self.width = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0][0] + 20  # Calculate width based on text size
        self.height = height
        self.text = text

class ToggleBtns:
    def __init__(self, x, y, btn_height, toggle_btns_textes, base_color, toggled_color, font_color):
        self.btns = []
        for i, text in enumerate(toggle_btns_textes):
            x_pos = x
            y_pos = y + i * (btn_height + 10)  # Adjust spacing dynamically
            self.btns.append(ToggleBtn(x_pos, y_pos, btn_height, text))  # Add ToggleBtn objects

        self.base_color = base_color
        self.toggled_color = toggled_color
        self.toggled = 0

    def draw(self, image):
        # Draw the button with transparency (50%)
        overlay = image.copy()
        for i, btn in enumerate(self.btns):
            color = self.toggled_color if self.toggled == i else self.base_color
            Draw.rounded_rectangle(overlay, (btn.x, btn.y), (btn.x + btn.width, btn.y + btn.height), 10, color, -1)
            cv2.putText(overlay, btn.text, (btn.x + 10, btn.y + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    def handle_click(self, pos):
        if pos is None or pos[0] is None or pos[1] is None:
            return False

        if self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + self.height:
            if self.clicked:
                return False
            self.toggled = not self.toggled
            self.current_text = self.text2 if self.toggled else self.text1
            self.clicked = True
            return True

        self.clicked = False
        return False