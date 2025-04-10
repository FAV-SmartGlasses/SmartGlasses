import cv2

class Button:
    def __init__(self, icon, x, y, text, base_color, hovering_color, size):
        self.icon = icon  # This should be a small cv2 image (numpy array)
        self.x_pos = x
        self.y_pos = y
        self.text = text
        self.base_color = base_color  # (B, G, R)
        self.hovering_color = hovering_color  # (B, G, R)
        self.size = size  # (width, height)
        self.rect = (x, y, x + size[0], y + size[1])  # (x1, y1, x2, y2)
        self.is_hovered = False

    def update(self, frame, cursor_pos):
        self.change_color(cursor_pos)
        # Draw button background
        color = self.hovering_color if self.is_hovered else self.base_color
        x1, y1, x2, y2 = self.rect
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, -1)

        # Draw icon if available
        if self.icon is not None:
            icon_resized = cv2.resize(self.icon, (30, 30))
            frame[y1 + 5:y1 + 35, x1 + 5:x1 + 35] = icon_resized

        # Draw text
        font_scale = 0.6
        thickness = 1
        font = cv2.FONT_HERSHEY_SIMPLEX
        text_size = cv2.getTextSize(self.text, font, font_scale, thickness)[0]
        text_x = x1 + 40
        text_y = y1 + (self.size[1] + text_size[1]) // 2 - 5
        cv2.putText(frame, self.text, (text_x, text_y), font, font_scale, (255, 255, 255), thickness)

    def check_for_input(self, position):
        x1, y1, x2, y2 = self.rect
        if x1 <= position[0] <= x2 and y1 <= position[1] <= y2:
            return True
        return False

    def change_color(self, position):
        self.is_hovered = self.check_for_input(position)