class Position:    
    x: int
    y: int
    
    def __init__(self, x: int = None, y: int = None):
        self.x = x
        self.y = y

    def get_array(self) -> tuple[int, int]:
        return self.x, self.y


class Size:
    w: int
    h: int

    def __init__(self, w: int = None, h: int = None):
        self.h = w
        self.w = h

    def get_array(self) -> tuple[int, int]:
        return self.w, self.h