from abc import ABC, abstractmethod
import numpy as np

from other_utilities import Position, Size

class Page(ABC):
    @abstractmethod
    def __init__(self):
        self._position: Position
        self._size: Size

    @abstractmethod
    def draw(self, image_overlay: np.ndarray,
             left_click_gesture_detected: bool, right_click_gesture_detected: bool, 
             left_cursor_position: tuple[int, int], right_cursor_position: tuple[int, int]):
        raise NotImplementedError("This method should be overridden in subclasses") 
    

class FixedAspectPage(Page):
    @abstractmethod
    def __init__(self):
        super().__init__()
        
        self.aspect_ratio: int
           
#region computing and setting size
    @abstractmethod
    def compute_aspect_ratio(self):
        if self.does_have_aspect_ratio:
            raise NotImplementedError

    def set_width(self, w):
        h = int(w / self.aspect_ratio)
        self._size = Size(w, h)

    def set_height(self, h):
        w = int(h * self.aspect_ratio)
        self._size = Size(w, h)
#endregion    


class FreeResizePage(Page):
    @abstractmethod
    def __init__(self):
        super().__init__()

    def set_size(self, w, h):
        self._size = Size(w, h)