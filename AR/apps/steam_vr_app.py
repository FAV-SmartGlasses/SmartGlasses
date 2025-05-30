from apps.app_base import FreeResizeApp
from gui.draw import *
from gui.keyboard import Keyboard


class SteamVR(FreeResizeApp):
    def __init__(self, name: str, display_name: str, icon_path: str):
        super().__init__(name, display_name, icon_path)

        self.keyboard = Keyboard([], "")
        self.keyboard.set_colors(get_neutral_color_bgra(), get_neutral_color2_bgra(), get_font_color_bgra(), 
                                get_neutral_color2_bgra(), get_nice_color_bgra(), get_nice_color_bgra())
        
        
        # Define IP and port
        IP = "0.0.0.0"  # Listen on all interfaces
        PORT = 31000

    def draw(self, image, gestures):
        cv2.setUseOptimized(True)

        if self.opened:
            self.check_fist_gesture(gestures)
            self.draw_lines(image, gestures)

            overlay = image.copy()

            # Draw the keyboard
            self.keyboard.draw(overlay, gestures)

            cv2.addWeighted(overlay, 0.5, image, 0.5, 0, image)