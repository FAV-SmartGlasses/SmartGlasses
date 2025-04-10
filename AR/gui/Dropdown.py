import cv2

class Dropdown:
    def __init__(self, x, y, width, height, options, base_color, hover_color, text_color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.options = options
        self.selected_option = options[0]
        self.base_color = base_color
        self.hover_color = hover_color
        self.text_color = text_color

        self.is_open = False
        self.hover_index = -1

    def draw(self, frame):
        # Draw main dropdown box
        main_color = self.hover_color if self.hover_index == -1 and self.is_open else self.base_color
        cv2.rectangle(frame, (self.x, self.y), (self.x + self.width, self.y + self.height), main_color, -1)
        self._draw_text(frame, self.selected_option, self.x + 10, self.y + self.height // 2 + 5)

        # Draw dropdown options if open
        if self.is_open:
            for i, option in enumerate(self.options):
                y_i = self.y + (i + 1) * self.height
                color = self.hover_color if self.hover_index == i else self.base_color
                cv2.rectangle(frame, (self.x, y_i), (self.x + self.width, y_i + self.height), color, -1)
                self._draw_text(frame, option, self.x + 10, y_i + self.height // 2 + 5)

    def _draw_text(self, frame, text, x, y):
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.6
        thickness = 1
        cv2.putText(frame, text, (x, y), font, font_scale, self.text_color, thickness)

    def handle_mouse(self, event, x, y, flags, param):
        if event == cv2.EVENT_MOUSEMOVE:
            self._update_hover(x, y)
        elif event == cv2.EVENT_LBUTTONDOWN:
            self._click(x, y)

    def _update_hover(self, x, y):
        self.hover_index = -1
        if self.is_open:
            for i in range(len(self.options)):
                y_i = self.y + (i + 1) * self.height
                if self.x <= x <= self.x + self.width and y_i <= y <= y_i + self.height:
                    self.hover_index = i
                    return
        elif self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height:
            self.hover_index = -1  # hovering main button

    def _click(self, x, y):
        if self.is_open:
            for i in range(len(self.options)):
                y_i = self.y + (i + 1) * self.height
                if self.x <= x <= self.x + self.width and y_i <= y <= y_i + self.height:
                    self.selected_option = self.options[i]
                    self.is_open = False
                    return
        if self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height:
            self.is_open = not self.is_open
        else:
            self.is_open = False  # click outside

    def get_selected(self):
        return self.selected_option