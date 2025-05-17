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

def set_size_and_position_by_ratio(page_position: Position, page_size: Size, 
                                   object_percent_position: Position, object_percent_size: Size) -> tuple[Position, Size]:

    w = int(object_percent_size.w / 100 * page_size.w)
    h = int(object_percent_size.h / 100 * page_size.h)
    
    x_on_page = int(object_percent_position.x / 100 * page_size.w)
    y_on_page = int(object_percent_position.y / 100 * page_size.h)

    x = x_on_page + page_position.x
    y = y_on_page + page_position.y

    return Position(x, y), Size(w, h)

def get_difference_between_positions(pos1: Position, pos2: Position) -> Position:
    #if pos1 is bigger than pos2, will be returned positive differences
    diff_x = pos1.x - pos2.x
    diff_y = pos1.y - pos2.y

    return Position(diff_x, diff_y)

def get_sum_of_positions(pos1: Position, pos2: Position) -> Position:
    diff_x = pos1.x - pos2.x
    diff_y = pos1.y - pos2.y

    return Position(diff_x, diff_y)

def get_sum_of_size_and_position(size: Size, position: Position) -> Size:
    w = size.w - position.x
    h = size.h - position.y

    return Size(w, h)