from abc import ABC, abstractmethod

import numpy as np

from other_utilities import Position, Size


class Element(ABC):
    @abstractmethod
    def __init__(self, position: Position, size: Size):
        self._position = position
        self._size = size

    def set_position_and_size(self, position: Position, size: Size):
        self._position = position
        self._size = size

    @abstractmethod
    def draw(self, image: np.ndarray):
        raise NotImplementedError("This method should be overridden in subclasses") 