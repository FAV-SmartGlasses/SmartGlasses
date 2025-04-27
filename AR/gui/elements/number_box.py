from .element_base import Element
from other_utilities import Position, Size

class NumberBox(Element):
    def __init__(self, position: Position, size:Size, step: float=1, min_value: float=None, max_value: float=None):
        super().__init__(position, size)
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.value = min_value

    def draw(self, image):
        return super().draw(image)

    def set_value(self, value):
        if self.min_value <= value <= self.max_value:
            self.value = value
        else:
            raise ValueError(f"Value must be between {self.min_value} and {self.max_value}.")