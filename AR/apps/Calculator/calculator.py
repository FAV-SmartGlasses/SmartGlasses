import numpy as np

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
            overlay = np.zeros((h, w, 4), dtype=np.uint8)
            """draw_rounded_rectangle(overlay,
                                self.position, 
                                (self.position[0] + self.size[0], self.position[1] + self.size[1]),
                                30, 
                                get_nice_color_bgra(),  # Use BGRA color
                                -1)"""
            


            #overlay = 
            self.pages[self.current_page].dynamic_draw(w, h, overlay,
                                                        left_click_gesture_detected, right_click_gesture_detected, 
                                                        left_cursor_position, right_cursor_position)
            
            """# Extrahujte RGB a alfa kanály
            rgb1, alpha1 = overlay[..., :3], overlay[..., 3] / 255.0
            rgb2, alpha2 = overlay[..., :3], overlay[..., 3] / 255.0

            # Vypočtěte výsledný alfa kanál
            alpha_result = alpha1 + alpha2 * (1 - alpha1)

            # Vypočtěte výslednou RGB hodnotu
            rgb_result = (rgb1 * alpha1[..., np.newaxis] + rgb2 * alpha2[..., np.newaxis] * (1 - alpha1[..., np.newaxis])) / alpha_result[..., np.newaxis]

            # Sloučte RGB a alfa kanál zpět do jednoho obrázku
            merged_overlay = np.dstack((rgb_result, (alpha_result * 255).astype(np.uint8)))"""
            
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
