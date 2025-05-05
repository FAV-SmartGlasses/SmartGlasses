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
        self.h = h
        self.w = w

    def get_array(self) -> tuple[int, int]:
        return self.w, self.h
    

def get_right_bottom_pos(position: Position, size: Size)-> Position:
    x1, x2 = position.x + size.w, position.y + size.h
    return Position(x1, x2)