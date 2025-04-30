from enum import Enum
from other_utilities import Position

class SwipeGesture(Enum):
    NO = 0
    RIGHT = 1
    LEFT = 2
    DOWN = 3
    UP = 4
    BOTH_RIGHT = 5
    BOTH_LEFT = 6
    BOTH_DOWN = 7
    BOTH_UP = 8
    BOTH_OUT = 9
    BOTH_IN = 10


class HandModel:
    def __init__(self, clicked: bool = False, 
                        cursor: Position = Position()):
        
        self.clicked: bool = clicked
        self.cursor: Position = cursor


class DetectionModel:
    def __init__(self, left_hand: HandModel = HandModel(),
                        right_hand: HandModel = HandModel(),
                        swipe_gesture: SwipeGesture = SwipeGesture.NO):
        
        self.left_hand: HandModel = left_hand
        self.right_hand: HandModel = right_hand
        self.swipe: SwipeGesture = swipe_gesture