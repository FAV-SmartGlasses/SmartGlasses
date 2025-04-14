import cv2

from menu_items import App
from gui.color_manager import *
from gui.draw import *
from gui.elements.button import Button

class Settings(App):
    def __init__(self, name, display_name, icon_path):
        super().__init__(name, display_name, icon_path)
        self.position = (100, 100)  # Pozice aplikace na obrazovce
        self.size = (400, 400)  # Velikost aplikace
        self.btn = Button(None, 200, 100, "Settings", (100, 100),
                          get_nice_color(), get_font_color(), 
                          get_font_color(), get_nice_color(), 
                          get_nice_color(), get_font_color())

    def draw(self, image, w, h, 
             left_click_gesture_detected, right_click_gesture_detected, 
             left_cursor_position, right_cursor_position):
        if self.opened:
            overlay = image.copy()

            draw_rounded_rectangle(overlay,
                                    self.position, 
                                    (self.position[0] + self.size[0], self.position[1] + self.size[1]),
                                    30, 
                                    get_nice_color(), 
                                    -1)
            
            # Kombinace původního obrázku a překryvného obrázku s průhledností
            alpha = 0.5  # Nastavení průhlednosti (0.0 = zcela průhledné, 1.0 = zcela neprůhledné)
            cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)

            self.btn.draw(image, False)
        
            #TODO: implementace vykreslení aplikace nastavení
        
        return image