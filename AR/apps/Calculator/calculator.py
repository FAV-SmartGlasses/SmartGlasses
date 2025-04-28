import numpy as np
import cv2
from PIL import Image

from apps.Calculator.page_converter import Converter
from apps.Calculator.page_standard_calculator import Standard
from apps.app_base import FixedAspectApp
from gui.draw import *
from gui.elements.dropdown import Dropdown
from other_utilities import Position, Size
from hand_detection_models import *

MAX_LENGTH = 10

class Calculator(FixedAspectApp):
    def __init__(self, name: str, display_name: str, icon_path: str):
        super().__init__(name, display_name, icon_path)
        
        self.pages = [
            Standard(),
            Converter()
        ]
        self.current_page = 0
        self.dropdown = Dropdown(Position(self._position.x + 200, self._position.y + 50), Size(200, 35), ["Standard", "Converter"], 0)

    def compute_aspect_ratio(self):
        pass

    def draw(self, image: np.ndarray, gestures: DetectionModel):
        
        cv2.setUseOptimized(True)
        
        if self.opened:
            h, w, _ = image.shape
            overlay = np.zeros((h, w, 4), dtype=np.uint8)
            """draw_rounded_rectangle(overlay,
                                self.position, 
                                (self.position[0] + self.size[0], self.position[1] + self.size[1]),
                                30, 
                                get_nice_color_bgra(),  # Use BGRA color
                                -1)"""

            #page_overlay = np.zeros((h, w, 4), dtype=np.uint8)
            page_w = w - 100
            self.pages[self.current_page].set_width(page_w)
            #overlay = 
            self.pages[self.current_page].draw(overlay, gestures)
            
            #overlay = self.alpha_blend(overlay, page_overlay)
            """page_overlay = self.insert_overlay(page_overlay, 50, 50, w, h)
            
            overlay = self.blend_overlays(overlay, page_overlay)"""
            
            self.dropdown.draw(image, gestures)
            
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


    def blend_overlays(self, bottom: np.ndarray, top: np.ndarray) -> np.ndarray:
        """
        Sloučí dva RGBA obrázky stejných rozměrů pomocí alfa kompozice.
        :param bottom: Spodní obrázek (RGBA)
        :param top: Vrchní obrázek (RGBA)
        :return: Nový obrázek (RGBA) po sloučení
        """
        if bottom.shape != top.shape:
            raise ValueError("Oba obrázky musí mít stejné rozměry a 4 kanály (RGBA).")

        # Převedeme alfa kanály do rozsahu 0–1
        alpha_top = top[:, :, 3:4] / 255.0
        alpha_bottom = bottom[:, :, 3:4] / 255.0

        # Výpočet výsledné RGB složky
        out_rgb = (top[:, :, :3] * alpha_top + bottom[:, :, :3] * alpha_bottom * (1 - alpha_top)) / (
            alpha_top + alpha_bottom * (1 - alpha_top) + 1e-6
        )

        # Výpočet výsledného alfa kanálu
        out_alpha = alpha_top + alpha_bottom * (1 - alpha_top)

        # Spojení RGB a Alpha do jednoho obrázku
        result = np.zeros_like(bottom, dtype=np.uint8)
        result[:, :, :3] = np.clip(out_rgb, 0, 1) * 255
        result[:, :, 3] = np.clip(out_alpha, 0, 1)[:, :, 0] * 255

        return result.astype(np.uint8)