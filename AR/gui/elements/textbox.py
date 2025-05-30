from abc import ABC

from other_utilities import Position, Size
from .element_base import Element


class TextBox(Element, ABC):
    def __init__(self, position: Position, size: Size, value: str, placeholder: str):
        super().__init__(position, size)
        self.value = value
        self.placeholder = placeholder