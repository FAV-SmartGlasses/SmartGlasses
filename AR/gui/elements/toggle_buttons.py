from gui.draw import *
from gui.elements.element_base import Element
from other_utilities import Position, Size


class ToggleButton(Element):
    def __init__(self, position: Position, height, text):
        width = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0][0] + 20  # Calculate width based on text size
        super().__init__(position, Size(width, height))
        self.text = text

    def draw(self, image, toggled = False):
        """background_color = get_nice_color() if toggled else (0, 0, 255)  # Green if toggled, red if not
        draw_rounded_rectangle(image, self.position, (self.position[0] + self.size[0], self.position[0] + self.size[1]), 10, (0, 0, 0), -1)
        cv2.putText(image, self.text, (self.x + 10, self.y + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)"""

        
        background_color = get_nice_color() if toggled else get_neutral_color()
        draw_rounded_rectangle(image, 
                                (self._position.x, self._position.y), 
                                (self._position.x + self._size.w, self._position.y + self._size.h), 
                                10, background_color, -1)
        cv2.putText(image, self.text, (self._position.x + 10, self._position.y + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        return image

class ToggleButtons(Element):
    def __init__(self, text: str, position: Position, button_height: int, toggle_buttons_texts: list[str]):
        height = (button_height + 10) * len(toggle_buttons_texts)
        width = max([cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0][0] for text in toggle_buttons_texts]) + 20
        super().__init__(position, Size(width, height))
        self.text = text
        self.clicked = None
        self.buttons = []
        for i, text in enumerate(toggle_buttons_texts):
            x_pos = position.x
            y_pos = position.y + i * (button_height + 10)  # Adjust spacing dynamically
            self.buttons.append(ToggleButton(Position(x_pos, y_pos), button_height, text))  # Add ToggleButton objects

        self.toggled = 0

    def draw(self, image, toggled = False):
        # Draw the button with transparency (50%)
        overlay = image.copy()

        draw_rounded_rectangle(overlay, (self._position.x, self._position.y), 
                               (self._position.x + self._size.w, self._position.y + self._size.h), 
                               10, get_nice_color(), -1)

        alpha = 0.5
        cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)

        for i, button in enumerate(self.buttons):
            toggled = i == self.toggled
            button.draw(image, toggled)

    def handle_click(self, pos: Position):
        if pos is None or pos.x is None or pos.y is None:
            return False

        if self.x <= pos.x <= self.x + self.width and self.y <= pos.y <= self.y + self.height:
            if self.clicked:
                return False
            self.toggled = not self.toggled
            self.current_text = self.text2 if self.toggled else self.text1
            self.clicked = True
            return True

        self.clicked = False
        return False