from gui.draw import *
from .element_base import Element


class Dropdown(Element):
    def __init__(self, position, size, options, selected_option=None):
        super().__init__(position, size)
        self.open = False
        self.options = options
        self.selected_option = selected_option
        self.padding = 10
        self.click_history = []

    def draw(self, image, w, h, left_click_gesture_detected, right_click_gesture_detected, 
             left_cursor_position, right_cursor_position): # TODO: teach Thomas how function overriding works
        
        is_left_hovered = is_cursor_in_rect(left_cursor_position, (self.position[0], self.position[1], self.position[0] + self.size[0], self.position[1] + self.size[1]))
        is_right_hovered = is_cursor_in_rect(right_cursor_position, (self.position[0], self.position[1], self.position[0] + self.size[0], self.position[1] + self.size[1]))
        is_left_clicked = is_left_hovered and left_click_gesture_detected
        is_right_clicked = is_right_hovered and right_click_gesture_detected
        is_clicked = is_left_clicked or is_right_clicked

        if is_clicked:
            if len(self.click_history) == 0 or (len(self.click_history) != 0 and self.click_history[-1] == False):
                self.open = not self.open
                self.click_history.append(True)
        else:
            if len(self.click_history) == 0 or (len(self.click_history) != 0 and self.click_history[-1]):
                self.click_history.append(False)
        

        text = self.selected_option if self.selected_option else "Select an option"
        self.draw_element(image, text)

        if self.open:
            for idx, option in enumerate(self.options):
                option_x = self.position[0]
                option_y = self.position[1] + (idx + 1) * (self.size[1] + self.padding)

                # Zkontrolujeme, jestli je kurzor nad možností
                rect = (option_x, option_y, option_x + self.size[0], option_y + self.size[1])
                hovered = False
                if is_cursor_in_rect(left_cursor_position, rect) or is_cursor_in_rect(right_cursor_position, rect):
                    hovered = True

                    if (left_click_gesture_detected and is_cursor_in_rect(left_cursor_position, rect)) or (right_click_gesture_detected and is_cursor_in_rect(right_cursor_position, rect)):
                        self.selected_option = option
                        self.open = False

                self.draw_option(image, option_x, option_y, hovered, option)
        
    def draw_element(self, image, text):
        size_y = self.size[1] * (len(self.options) + 1) + self.padding * (len(self.options) + 1) if self.open else self.size[1]
        draw_rounded_rectangle(image, self.position, (self.position[0] + self.size[0], self.position[1] + size_y), 15, get_nice_color(), -1)
        cv2.putText(image, text, (self.position[0] + 10, self.position[1] + 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, get_font_color(), 2)

    def draw_option(self, image, x, y, hovered, text):
        color = get_nice_color() if hovered else get_neutral_color()
        draw_rounded_rectangle(image, (x + self.padding, y), (x + self.size[0] - self.padding, y + self.size[1]), 15, color, -1)
        cv2.putText(image, text, (x + self.padding + 10, y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, get_font_color(), 2)