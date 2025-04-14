from draw import *

class Button:
    def __init__(self, icon, x, y, text, size, 
             color, border_color, font_color, hover_color, hover_border_color, hover_font_color):  # (B, G, R)
        
        self.icon = icon  # This should be a small cv2 image (numpy array)
        self.text = text

        self.x_pos = x
        self.y_pos = y
        self.size = size  # (width, height)
        self.rect = (x, y, x + size[0], y + size[1])  # (x1, y1, x2, y2)

        self.is_hovered = False
        self.color = color  # (B, G, R)
        self.border_color = border_color
        self.font_color = font_color
        self.hovering_color = hover_color
        self.hovering_border_color = hover_border_color
        self.hovering_font_color = hover_font_color


    def draw(self, frame, is_hovered):
        self.is_hovered = is_hovered

        # setting colors based on hover state
        border_color = self.hovering_border_color if self.is_hovered else self.border_color
        font_color = self.hovering_font_color if self.is_hovered else self.font_color
        
        # Draw button background
        x1, y1, x2, y2 = self.rect
        draw_rounded_rectangle(frame, (x1, y1), (x2, y2), 10, (0, 0, 255), -1)
        draw_rounded_rectangle(frame, (x1, y1), (x2, y2), 10, border_color, 2)

        # Draw icon if available
        if self.icon is not None:
            icon_resized = cv2.resize(self.icon, (30, 30))
            frame[y1 + 5:y1 + 35, x1 + 5:x1 + 35] = icon_resized

        # Draw text if available
        if self.text is not None:
            font_scale = 0.6
            thickness = 1
            font = cv2.FONT_HERSHEY_SIMPLEX
            text_size = cv2.getTextSize(self.text, font, font_scale, thickness)[0]
            text_x = x1 + (self.size[0] - text_size[0]) // 2
            text_y = y1 + (self.size[1] + text_size[1]) // 2 - 5
            cv2.putText(frame, self.text, (text_x, text_y), font, font_scale, font_color, thickness)