import numpy as np
import cv2
from PIL import Image

from apps.Calculator.page_converter import Converter
from apps.Calculator.page_standard_calculator import Standard
from apps.app_base import App
from gui.draw import *
from gui.elements.dropdown import Dropdown

MAX_LENGTH = 10

class Calculator(App):
    def __init__(self, name: str, display_name: str, icon_path: str):
        super().__init__(name, display_name, icon_path)
        
        self.pages = [
            Standard(),
            Converter()
        ]
        self.current_page = 0
        self.dropdown = Dropdown((self.position[0] + 200, self.position[1] + 50), (200, 35), ["Standard", "Converter"], 0)

    def draw(self, image: np.ndarray, w: int, h: int, 
             left_click_gesture_detected: bool, right_click_gesture_detected: bool, 
             left_cursor_position: tuple[int, int], right_cursor_position: tuple[int, int]):
        
        if self.opened:
            #self.size = 

            overlay = np.zeros((h, w, 4), dtype=np.uint8)
            #image_pil = Image.fromarray(overlay, mode="RGBA")  # nebo "RGB" podle kanálů
            #image_pil.save("overlay1.png")
            """draw_rounded_rectangle(overlay,
                                self.position, 
                                (self.position[0] + self.size[0], self.position[1] + self.size[1]),
                                30, 
                                get_nice_color_bgra(),  # Use BGRA color
                                -1)"""
            
            #image_pil = Image.fromarray(overlay, mode="RGBA")  # nebo "RGB" podle kanálů
            #image_pil.save("overlay2.png")


            #page_overlay = np.zeros((h, w, 4), dtype=np.uint8)
            page_w = w - 100
            page_h = h - 100
            self.pages[self.current_page].set_width(page_w)
            page_overlay = self.pages[self.current_page].draw(overlay, 
                                                                    left_click_gesture_detected, right_click_gesture_detected, 
                                                                    left_cursor_position, right_cursor_position)
            #image_pil = Image.fromarray(page_overlay, mode="RGBA")  # nebo "RGB" podle kanálů
            #image_pil.save("page_overlay.png")
            
            overlay = self.alpha_blend(overlay, page_overlay)
            """page_overlay = self.insert_overlay(page_overlay, 50, 50, w, h)
            
            #image_pil = Image.fromarray(page_overlay, mode="RGBA")  # nebo "RGB" podle kanálů
            #image_pil.save("page_overlay_bigger.png")
            #overlay = self.alpha_blend(overlay, page_overlay)
            overlay = self.blend_overlays(overlay, page_overlay)"""
            #image_pil = Image.fromarray(overlay, mode="RGBA")  # nebo "RGB" podle kanálů
            #image_pil.save("overlay_3.png")
            
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

            
            #image_pil = Image.fromarray(image, mode="RGB")  # nebo "RGB" podle kanálů
            #image_pil.save("image1.png")
            # Blend overlay onto image using OpenCV
            alpha_channel = (overlay[:, :, 3] / 255.0) * get_app_transparency()  # Adjust alpha channel by transparency factor
            alpha_channel = np.clip(alpha_channel, 0, 1)  # Ensure alpha values are within [0, 1]
            for c in range(3):  # Blend RGB channels
                image[y_offset:y_offset + overlay_h, x_offset:x_offset + overlay_w, c] = (
                    alpha_channel * overlay[:, :, c] +
                    (1 - alpha_channel) * image[y_offset:y_offset + overlay_h, x_offset:x_offset + overlay_w, c]
                )

            
            #image_pil = Image.fromarray(image, mode="RGB")  # nebo "RGB" podle kanálů
            #image_pil.save("image2.png")

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

    def alpha_blend(self, overlay_bottom: np.ndarray, overlay_top: np.ndarray) -> np.ndarray:
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
    
    def insert_overlay(self, overlay: np.ndarray, x_offset: int, y_offset: int, w: int, h: int) -> np.ndarray:
        new_overlay = np.zeros((h, w, 4), dtype=np.uint8)
        H, W, _ = overlay.shape

        for y in range(H):
            for x in range(W):
                new_x = x + x_offset
                new_y = y + y_offset
                if 0 <= new_x < w and 0 <= new_y < h:
                    new_overlay[new_y, new_x] = overlay[y, x]

        return new_overlay
        
        output = np.zeros((h, w, 4), dtype=np.uint8)

        oh, ow = overlay.shape[:2]

        # Vypočítání hranic pro vložení s oříznutím, pokud je potřeba
        x1 = max(x, 0)
        y1 = max(y, 0)
        x2 = min(x + ow, w)
        y2 = min(y + oh, h)

        # Odpovídající oblast ve zdroji (page_overlay)
        src_x1 = max(0, -x)
        src_y1 = max(0, -y)
        src_x2 = src_x1 + (x2 - x1)
        src_y2 = src_y1 + (y2 - y1)

        if x1 < x2 and y1 < y2:
            output[y1:y2, x1:x2] = overlay[src_y1:src_y2, src_x1:src_x2]

        return output