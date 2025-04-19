from .element_base import Element

class NumberBox(Element):
    def __init__(self, position, size, min_value=0, max_value=100, step=1):
        super().__init__(position, size)
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.value = min_value  # Initialize value to min_value

    def draw(self, image, w, h):
        # Placeholder for drawing logic
        pass

    def set_value(self, value):
        if self.min_value <= value <= self.max_value:
            self.value = value
        else:
            raise ValueError(f"Value must be between {self.min_value} and {self.max_value}.")