import cv2
from draw import *

class Button:
    def __init__(self, icon, x, y, text, size, 
             color, border_color, font_color, hover_color, hover_border_color, hover_font_color):  # (B, G, R)
        
        self.icon = icon  # This should be a small cv2 image (numpy array)
        self.x_pos = x
        self.y_pos = y
        self.text = text

        self.color = color  # (B, G, R)
        self.border_color = border_color
        self.font_color = font_color
        self.hovering_color = hover_color
        self.hovering_border_color = hover_border_color
        self.hovering_font_color = hover_font_color

        self.size = size  # (width, height)
        self.rect = (x, y, x + size[0], y + size[1])  # (x1, y1, x2, y2)
        self.is_hovered = False

    def update(self, frame):
        self.is_hovered = self.check_for_input((self.x_pos, self.y_pos))

        # Draw button background
        color = self.hovering_color if self.is_hovered else self.color
        border_color = self.hovering_border_color if self.is_hovered else self.border_color
        font_color = self.hovering_font_color if self.is_hovered else self.font_color
        
        x1, y1, x2, y2 = self.rect
        #cv2.rectangle(frame, (x1, y1), (x2, y2), color, -1)
        draw_rounded_rectangle(frame, (x1, y1), (x2, y2), 10, color, -1)
        draw_rounded_rectangle(frame, (x1, y1), (x2, y2), 10, border_color, 2)

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
        cv2.putText(frame, self.text, (text_x, text_y), font, font_scale, font_color, thickness)

    def check_for_input(self, position):
        if position  == (None, None):
            return False
        
        x1, y1, x2, y2 = self.rect
        if x1 <= position[0] <= x2 and y1 <= position[1] <= y2:
            return True
        
        return False