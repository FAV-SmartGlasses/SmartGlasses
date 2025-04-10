from enum import Enum

from menu_items import App


class Settings(App):
    def __init__(self, name, display_name, icon_path):
        super().__init__(name, display_name, icon_path)
        self.opened = True  # Nastavení aplikace jako otevřené
        self.position = (0, 0)  # Pozice aplikace na obrazovce
        self.size = (300, 300)  # Velikost aplikace

        self.theme = self.Theme.LIGHT
        self.language = self.Language.ENGLISH
        self.saved_wifi = {}
        self.saved_bluetooth_devices = {}
        self.airplane_mode_ON = False
        self.bluetooth_ON = True
        self.wifi_ON = True
        self.keyboard_layout = self.keyboard_layout.QWERTY_ENGLISCH
        self.volume = 50  # Hlasitost (0-100)
        self.microfon_ON = True
        self.brightness = 50  # Jas (0-100)
        self.assistent_ON = True  # Asistent zapnutý
        self.GPS_ON = True
        #TODO: implementace dalších nastavení headsetu


    class Theme(Enum):
        LIGHT = 0
        DARK = 1

    class Language(Enum):
        ENGLISH = 0
        CZECH = 1

    class keyboard_layout(Enum):
        QWERTY_ENGLISCH = 0
        AZERTY_ENGLISCH = 1
        QWERTZ_ENGLISCH = 2
        QWERTY_CZECH = 4
        AZERTY_CZECH = 5
        QWERTZ_CZECH = 6

    def draw(self, image, w, h, click_gesture_detected, cursor_position):
        if not self.opened:
            return image
        
        #TODO: implementace vykreslení aplikace nastavení
        
        return image
    
    def get_theme(self):
        return self.theme