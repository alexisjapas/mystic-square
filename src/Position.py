from typing import ClassVar


class Position:
    cell_size: ClassVar[int] = 32

    def __init__(self, x, y):
        self.x = x
        self.y = y
