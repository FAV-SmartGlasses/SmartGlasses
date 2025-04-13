from enum import Enum

from menu_items import App


class Settings(App):
    def __init__(self, name, display_name, icon_path):
        super().__init__(name, display_name, icon_path)
        self.opened = True  # Nastavení aplikace jako otevřené
        self.position = (0, 0)  # Pozice aplikace na obrazovce
        self.size = (300, 300)  # Velikost aplikace

    def draw(self, image, w, h, click_gesture_detected, cursor_position):
        if not self.opened:
            return image
        
        #TODO: implementace vykreslení aplikace nastavení
        
        return image
    
    def get_theme(self):
        return self.theme