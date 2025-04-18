import numpy as np
from apps.Calculator.page_converter import Converter
from apps.Calculator.page_standart_calculator import Standard
from apps.app_base import App
from settings_manager import *

MAX_LENGTH = 10

class Calculator(App):
    def __init__(self, name, display_name, icon_path):
        super().__init__(name, display_name, icon_path)
        
        self.pages = [
            Standard(),
            Converter()
        ]
        self.current_page = 0

    def draw(self, image, w, h, 
             left_click_gesture_detected, right_click_gesture_detected, 
             left_cursor_position, right_cursor_position):
        
        if self.opened:
            overlay = self.pages[self.current_page].draw(w, h, image,
                            left_click_gesture_detected, right_click_gesture_detected, 
                            left_cursor_position, right_cursor_position)
            
            # Ensure overlay is smaller than image
            overlay_h, overlay_w, _ = overlay.shape
            image_h, image_w, _ = image.shape

            if overlay_w > image_w or overlay_h > image_h:
                raise ValueError("Overlay dimensions must be smaller than image dimensions.")

            # Calculate position to center overlay
            x_offset = (image_w - overlay_w) // 2
            y_offset = (image_h - overlay_h) // 2

            # Blend overlay onto image using OpenCV
            alpha_channel = (overlay[:, :, 3] / 255.0) * get_app_transparency()  # Adjust alpha channel by transparency factor
            alpha_channel = np.clip(alpha_channel, 0, 1)  # Ensure alpha values are within [0, 1]
            for c in range(3):  # Blend RGB channels
                image[y_offset:y_offset + overlay_h, x_offset:x_offset + overlay_w, c] = (
                    alpha_channel * overlay[:, :, c] +
                    (1 - alpha_channel) * image[y_offset:y_offset + overlay_h, x_offset:x_offset + overlay_w, c]
                )
