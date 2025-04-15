import cv2

from menu_items import App
from gui.color_manager import *
from gui.draw import *
from gui.elements.button import Button
from gui.elements.toggle_buttons import ToggleButtons

class Settings(App):
    def __init__(self, name, display_name, icon_path):
        super().__init__(name, display_name, icon_path)
        self.position = (100, 100)  # Pozice aplikace na obrazovce
        self.size = (400, 400)  # Velikost aplikace
        self.btn = Button(None, 300, 400, "Settings", (100, 50),
                          get_neutral_color(), get_neutral_color(), get_font_color(), 
                          get_nice_color(), get_neutral_color2(), get_font_color())
        self.toggle = ToggleButtons("neco", (self.position[0] + 10, self.position[1] + 10), 20, ["Option 1", "Option 2", "Option 3"])

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

            left_in_rect = is_cursor_in_rect(left_cursor_position, (self.btn.x_pos, self.btn.y_pos, self.btn.x_pos + self.btn.size[0], self.btn.y_pos + self.btn.size[1]))
            right_in_rect = is_cursor_in_rect(right_cursor_position, (self.btn.x_pos, self.btn.y_pos, self.btn.x_pos + self.btn.size[0], self.btn.y_pos + self.btn.size[1]))
            
            is_in_rect = left_in_rect or right_in_rect

            self.btn.draw(image, is_in_rect)
            
            self.toggle.draw(image)
        
            #TODO: implementace vykreslení aplikace nastavení
        
        return image