import cv2


class ToggleButton:
    def __init__(self, x, y, width, height, text1, text2, base_color, toggled_color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text1 = text1
        self.text2 = text2
        self.base_color = base_color
        self.toggled_color = toggled_color
        self.toggled = False
        self.clicked = False
        self.current_text = self.text1  # Initial text is text1

    def draw(self, image):
        # Draw the button with transparency (50%)
        overlay = image.copy()
        button_color = self.toggled_color if self.toggled else self.base_color
        cv2.rectangle(overlay, (self.x, self.y), (self.x + self.width, self.y + self.height), button_color, -1)
        cv2.addWeighted(overlay, 0.5, image, 0.5, 0, image)  # 50% transparency for toggle button

        # Button border and text
        cv2.rectangle(image, (self.x, self.y), (self.x + self.width, self.y + self.height), (0, 0, 0), 2)
        cv2.putText(image, self.current_text, (self.x + 10, self.y + int(self.height * 0.7)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

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