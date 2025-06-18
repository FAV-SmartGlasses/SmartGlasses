from gui.draw import *
from hand_detection_models import DetectionModel
from other_utilities import Position, Size
from .element_base import Element


class Dropdown(Element):
    def __init__(self, position: Position, size: Size, options: list[str], selected_option_index: int = None, white_borders: bool = False):
        super().__init__(position, size)
        self.open: bool = False
        self.options: list[str] = options
        self.selected_option_index: int | None = selected_option_index
        self.padding = 10
        self.click_history: list[bool] = []
        self.selected_option : str = ""
        self.selected : bool = selected_option_index is not None
        self.white_borders: bool = white_borders

    def render(self, image: np.ndarray, gestures: DetectionModel):
        text = self.selected_option if self.selected else "Select"

        rect = (*self._position.get_array(), self._position.x + self.size.w, self._position.y + self.size.h)
        option_left_hovered = is_cursor_in_rect(gestures.left_hand.cursor, rect)
        option_right_hovered = is_cursor_in_rect(gestures.right_hand.cursor, rect)
        hovered = option_left_hovered or option_right_hovered
        self.draw_element(image, text, False if self.open else hovered)

        if self.open:
            for index, option in enumerate(self.options):
                option_x = self._position.x
                option_y = self._position.y + (index + 1) * (self.size.h + self.padding)

                rect = (option_x, option_y, option_x + self.size.w, option_y + self.size.h)
                option_left_hovered = is_cursor_in_rect(gestures.left_hand.cursor, rect)
                option_right_hovered = is_cursor_in_rect(gestures.right_hand.cursor, rect)
                hovered = option_left_hovered or option_right_hovered

                self.draw_option(image, option_x, option_y, hovered, option)

    def draw(self, image: np.ndarray, gestures: DetectionModel):
        # Check if the cursor is hovering over the main dropdown area
        is_left_hovered = is_cursor_in_rect(gestures.left_hand.cursor, (self._position.x, self._position.y, self._position.x + self.size.w, self._position.y + self.size.h))
        is_right_hovered = is_cursor_in_rect(gestures.right_hand.cursor, (self._position.x, self._position.y, self._position.x + self.size.w, self._position.y + self.size.h))
        is_hovered = is_left_hovered or is_right_hovered
        is_left_clicked = is_left_hovered and gestures.left_hand.clicked
        is_right_clicked = is_right_hovered and gestures.right_hand.clicked
        is_clicked = is_left_clicked or is_right_clicked

        self.selected = self.selected_option_index is not None

        if self.selected:
            self.selected_option = self.options[self.selected_option_index]
        else:
            self.selected_option = ""

        if is_clicked:
            if len(self.click_history) == 0 or (len(self.click_history) != 0 and self.click_history[-1] == False):
                self.open = not self.open
                self.click_history.append(True)
        else:
            if len(self.click_history) == 0 or (len(self.click_history) != 0 and self.click_history[-1]):
                self.click_history.append(False)

        # If the dropdown is open, check hover and click for each option
        if self.open:
            for index, option in enumerate(self.options):
                option_x = self._position.x
                option_y = self._position.y + (index + 1) * (self.size.h + self.padding)

                rect = (option_x, option_y, option_x + self.size.w, option_y + self.size.h)
                option_left_hovered = is_cursor_in_rect(gestures.left_hand.cursor, rect)
                option_right_hovered = is_cursor_in_rect(gestures.right_hand.cursor, rect)

                hovered = option_left_hovered or option_right_hovered

                # Draw the option with hover effect if applicable
                self.draw_option(image, option_x, option_y, hovered, option)

                # Select the option if clicked
                if ((gestures.left_hand.clicked and option_left_hovered) or 
                    (gestures.right_hand.clicked and option_right_hovered)):
                    self.selected_option_index = index
                    self.open = False

        # Render the dropdown
        self.render(image, gestures)

    def draw_element(self, image: np.ndarray, text: str, hovered: bool = False):
        size_y = self.size.h * (len(self.options) + 1) + self.padding * (len(self.options) + 1) if self.open else self.size.h
        color = get_nice_color() if not hovered else get_neutral_color2()
        draw_rounded_rectangle(image, (self._position.x, self._position.y), (self._position.x + self.size.w, self._position.y + size_y), 15, color, -1)
        if self.white_borders:
            draw_rounded_rectangle(image, (self._position.x, self._position.y), (self._position.x + self.size.w, self._position.y + size_y), 15, (255, 255, 255), 2)
        text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
        text_x = self._position.x + (self.size.w - text_size[0]) // 2
        text_y = self._position.y + (self.size.h + text_size[1]) // 2
        font_color = get_nice_color() if hovered else get_font_color()
        cv2.putText(image, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, font_color, 2)

    def draw_option(self, image: np.ndarray, x: int, y: int, hovered: bool, text: str):
        color = get_nice_color() if hovered else get_neutral_color()
        draw_rounded_rectangle(image, (x + self.padding, y), (x + self.size.w - self.padding, y + self.size.h), 15, color, -1)
        if self.white_borders and hovered:
            draw_rounded_rectangle(image, (x + self.padding, y), (x + self.size.w - self.padding, y + self.size.h), 15, (255, 255, 255), 2)
        text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
        text_x = x + (self.size.w - text_size[0]) // 2
        text_y = y + (self.size.h + text_size[1]) // 2
        cv2.putText(image, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, get_font_color(), 2)