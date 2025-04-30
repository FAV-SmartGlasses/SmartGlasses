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
from settings_manager import get_app_transparency

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
        self._position = Position(0, 0)
        #self._size = #500

    def compute_aspect_ratio(self):
        pass

    def draw(self, image: np.ndarray, gestures: DetectionModel):
        cv2.setUseOptimized(True)
        
        if self.opened:
            h, w, _ = image.shape
            overlay = image.copy()
            """draw_rounded_rectangle(overlay,
                                self.position, 
                                (self.position[0] + self.size[0], self.position[1] + self.size[1]),
                                30, 
                                get_nice_color_bgra(),  # Use BGRA color
                                -1)"""

            page_w = w - 100
            self.pages[self.current_page].set_width(page_w)
            #overlay = 
            self.pages[self.current_page].draw(overlay, gestures)
            
            self.dropdown.draw(overlay, gestures)

            # Kombinace původního obrázku a překryvného obrázku s průhledností
            alpha = get_app_transparency()
            cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)