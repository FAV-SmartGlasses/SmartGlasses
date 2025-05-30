from gui.draw import *
from hand_detection_models import DetectionModel
from other_utilities import *
from .element_base import Element


class NumberBox(Element):
    def __init__(self, position: Position, size: Size, step: float=1, min_value: float=None, max_value: float=None):
        super().__init__(position, size)
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.value = min_value

    def draw(self, overlay: np.ndarray, gestures: DetectionModel):
        draw_rounded_rectangle(overlay, 
                               self._position.get_array(), 
                               get_right_bottom_pos(self._position, self._size).get_array(), 
                               10, get_nice_color(), -1)
        text = str(self.value) if self.value is not None else ""
        text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
        text_x = self._position.x + (self._size.w - text_size[0])//2
        text_y = self._position.y + (self._size.h + text_size[1])//2
        cv2.putText(overlay, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, get_font_color_bgra(), 2)