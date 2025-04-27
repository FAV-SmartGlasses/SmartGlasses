from .element_base import Element
from other_utilities import Position, Size

class TextBox(Element):
    def __init__(self, position: Position, size: Size, value: str, placeholder: str):
        super().__init__(position, size)
        self.value = value
        self.placeholder = placeholder