class Element:
    def __init__(self, position, size):
        self.position = position
        self.size = size

    def draw(self, image, w, h, toggled = False):
        raise NotImplementedError("This method should be overridden in subclasses") 