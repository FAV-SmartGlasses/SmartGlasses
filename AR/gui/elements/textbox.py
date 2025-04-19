from .element_base import Element
from enum import Enum

class TextBox(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.value = kwargs.get("value", "")  # Default value is an empty string
        self.placeholder = kwargs.get("placeholder", "")  # Default placeholder is an empty string