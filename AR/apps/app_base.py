from abc import abstractmethod
import numpy as np

from menu_items import MenuItem
from other_utilities import Position, Size
from hand_detection_models import *
from other_utilities import *

class App(MenuItem):
    @abstractmethod
    def __init__(self, name, display_name, icon_path):
        super().__init__(name, display_name, icon_path)
        self.opened = False
        self._position: Position = Position(0, 0) # Pozice aplikace na obrazovce
        self._size: Size = Size(400, 400) # Velikost aplikace
        self.pages = []  # Seznam stránek aplikace
        self.current_page = 0  # Index aktuální stránky

    def add_page(self, page):
        self.pages.append(page)

    def switch_page(self, page_index):
        if 0 <= page_index < len(self.pages):
            self.current_page = page_index
        else:
            print(f"Invalid page index: {page_index}")

    def check_fist_gesture(self, gestures: DetectionModel):
        self._last_position = self._position
        if (gestures.right_hand.last_wrist_position.get_array() != (None,None) and 
            gestures.right_hand.fist == True and
            gestures.right_hand.wrist_position.get_array() != (None,None)):

            wrist_diff = get_difference_between_positions(gestures.right_hand.last_wrist_position, gestures.right_hand.wrist_position)
            self._position = get_sum_of_positions(self._position, wrist_diff)

#region Opening/closing app
    def clicked(self):
        super().clicked()
        if self.opened:
            self.close()
        else:
            self.launch()

    def launch(self):
        self.opened = True

    def close(self):
        self.opened = False

    def draw(self, image: np.ndarray, gestures: DetectionModel):
        return image
#endregion

class FixedAspectApp(App):
    def __init__(self, name, display_name, icon_path):
        super().__init__(name, display_name, icon_path)
        
        self.aspect_ratio: int
           
#region computing and setting size
    @abstractmethod
    def compute_aspect_ratio(self):
        if self.does_have_aspect_ratio:
            #implement
            raise NotImplementedError

    def set_width(self, w):
        h = int(w / self.aspect_ratio)
        self._size = Size(w, h)

    def set_height(self, h):
        w = int(h * self.aspect_ratio)
        self._size = Size(w, h)
#endregion    


class FreeResizeApp(App):
    def __init__(self, name, display_name, icon_path):
        super().__init__(name, display_name, icon_path)

    def set_size(self, w, h):
        self._size = Size(w, h)