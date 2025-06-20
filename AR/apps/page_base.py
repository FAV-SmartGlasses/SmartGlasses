from abc import ABC, abstractmethod

import numpy as np

from hand_detection_models import *
from other_utilities import Size


class Page(ABC):
    def __init__(self):
        self._position: Position | None = None
        self._size: Size | None = None

    @abstractmethod
    def draw(self, image_overlay: np.ndarray, gestures: DetectionModel):
        raise NotImplementedError("This method should be overridden in subclasses") 
    

class FixedAspectPage(Page):
    def __init__(self):
        super().__init__()
        
        self.aspect_ratio: int = self.compute_aspect_ratio()

    @abstractmethod
    def compute_aspect_ratio(self):
        raise NotImplementedError

    def set_width(self, w):
        h = int(w / self.aspect_ratio)
        self._size = Size(w, h)

    def set_height(self, h):
        w = int(h * self.aspect_ratio)
        self._size = Size(w, h)


class FreeResizePage(Page):
    @abstractmethod
    def __init__(self):
        super().__init__()

    def set_size(self, w, h):
        self._size = Size(w, h)