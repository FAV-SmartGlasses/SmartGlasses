from apps.app_base import FreeResizeApp
from gui.draw import *
from gui.elements.button import Button
from gui.elements.toggle_buttons import ToggleButtons
from hand_detection_models import DetectionModel
from other_utilities import Position, Size
from settings_manager import *


class Settings(FreeResizeApp):
    def __init__(self, name: str, display_name: str, icon_path: str):
        super().__init__(name, display_name, icon_path)
        self._position: Position = Position(100, 100)  # Pozice aplikace na obrazovce
        self._size: Size = Size(400, 400)  # Velikost aplikace
        self.button = Button(None, Position(300, 400), Size(100, 50), "Settings",
                          get_neutral_color(), get_neutral_color(), get_font_color(), 
                          get_nice_color(), get_neutral_color2(), get_font_color())
        self.toggle = ToggleButtons("neco", Position(self._position.x + 10, self._position.y + 10), 20, ["Option 1", "Option 2", "Option 3"])

    def draw(self, image: np.ndarray, gestures: DetectionModel):
        
        if self.opened:
            self.check_fist_gesture(gestures)
            self.draw_lines(image, gestures)

            overlay = image.copy()

            draw_rounded_rectangle(overlay,
                                    (self._position.x, self._position.y), 
                                    (self._position.x + self._size.w, self._position.y + self._size.h),
                                    30, 
                                    get_nice_color(), 
                                    -1)
            
            # Kombinace původního obrázku a překryvného obrázku s průhledností
            alpha = get_app_transparency()
            cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)

            left_in_rect = is_cursor_in_rect(gestures.left_hand.cursor, 
                                             (self.button._position.x, self.button._position.y, 
                                              self.button._position.x + self.button._size.w, self.button._position.y + self.button._size.h))
            right_in_rect = is_cursor_in_rect(gestures.right_hand.cursor, 
                                              (self.button._position.x, self.button._position.y, 
                                               self.button._position.x + self.button._size.w, self.button._position.y + self.button._size.h))
            
            is_in_rect = left_in_rect or right_in_rect

            self.button.draw(image, is_in_rect)
            
            self.toggle.draw(image)
        
            #TODO: implementace vykreslení aplikace nastavení