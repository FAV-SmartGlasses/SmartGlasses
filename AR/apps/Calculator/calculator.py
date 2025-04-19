import numpy as np
import cv2

from apps.Calculator.page_converter import Converter
from apps.Calculator.page_standard_calculator import Standard
from apps.app_base import App
from gui.draw import *
from gui.elements.dropdown import Dropdown

MAX_LENGTH = 10

class Calculator(App):
    def __init__(self, name, display_name, icon_path):
        super().__init__(name, display_name, icon_path)
        
        self.pages = [
            Standard(),
            Converter()
        ]
        self.current_page = 0
        self.dropdown = Dropdown((self.position[0] + 200, self.position[1] + 50), (200, 35), ["Standard", "Converter"], 0)

    def draw(self, image, w, h, 
             left_click_gesture_detected, right_click_gesture_detected, 
             left_cursor_position, right_cursor_position):
        
        if self.opened:
            #self.size = 

            overlay = np.zeros((h, w, 4), dtype=np.uint8)
            """draw_rounded_rectangle(overlay,
                                self.position, 
                                (self.position[0] + self.size[0], self.position[1] + self.size[1]),
                                30, 
                                get_nice_color_bgra(),  # Use BGRA color
                                -1)"""
            


            page_overlay = np.zeros((h, w, 4), dtype=np.uint8)
            self.pages[self.current_page].set_width(w)
            self.pages[self.current_page].dynamic_draw(page_overlay,
                                                        left_click_gesture_detected, right_click_gesture_detected, 
                                                        left_cursor_position, right_cursor_position)
            
            overlay = self.alpha_blend(overlay, page_overlay)
            
            self.dropdown.draw(image, w, h,
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

    def alpha_blend(self, overlay_bottom, overlay_top):
        # Předpokládáme stejnou velikost a formát (h, w, 4)
        alpha_top = overlay_top[:, :, 3] / 255.0
        alpha_bottom = overlay_bottom[:, :, 3] / 255.0

        out_rgb = np.zeros_like(overlay_top[:, :, :3], dtype=np.float32)
        for c in range(3):  # RGB kanály
            out_rgb[:, :, c] = (overlay_top[:, :, c] * alpha_top +
                                overlay_bottom[:, :, c] * alpha_bottom * (1 - alpha_top))

        out_alpha = alpha_top + alpha_bottom * (1 - alpha_top)
        out = np.dstack((out_rgb, out_alpha[:, :, np.newaxis] * 255)).astype(np.uint8)
        return out