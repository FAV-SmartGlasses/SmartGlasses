from draw import *

class ToggleButton:
    def __init__(self, x, y, height, text):
        self.x = x
        self.y = y
        self.width = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0][0] + 20  # Calculate width based on text size
        self.height = height
        self.text = text

class ToggleButtons:
    def __init__(self, x, y, button_height, toggle_buttons_textes, base_color, toggled_color, font_color):
        self.text1 = None
        self.text2 = None
        self.current_text = None
        self.height = None
        self.y = None
        self.width = None
        self.x = None
        self.clicked = None
        self.buttons = []
        for i, text in enumerate(toggle_buttons_textes):
            x_pos = x
            y_pos = y + i * (button_height + 10)  # Adjust spacing dynamically
            self.buttons.append(ToggleButton(x_pos, y_pos, button_height, text))  # Add ToggleButton objects

        self.base_color = base_color
        self.toggled_color = toggled_color
        self.toggled = 0

    def draw(self, image):
        # Draw the button with transparency (50%)
        overlay = image.copy()
        for i, button in enumerate(self.buttons):
            color = self.toggled_color if self.toggled == i else self.base_color
            draw_rounded_rectangle(overlay, (button.x, button.y), (button.x + button.width, button.y + button.height), 10, color, -1)
            cv2.putText(overlay, button.text, (button.x + 10, button.y + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

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