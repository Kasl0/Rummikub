from enum import Enum


class Color(Enum):
    Black = 1
    Blue = 2
    Red = 3
    Yellow = 4

    def __str__(self):

        if self.value == 1:
            return "Ba"
        if self.value == 2:
            return "Bu"
        if self.value == 3:
            return "R"
        if self.value == 4:
            return "Y"
