from enum import Enum
from arcade import color


class Color(Enum):

    Joker = 0
    Black = 1
    Blue = 2
    Red = 3
    Yellow = 4

    def get_arcade_color(self):

        if self.value == 0:
            return color.GREEN
        if self.value == 1:
            return color.BLACK
        if self.value == 2:
            return color.BLUE
        if self.value == 3:
            return color.RED
        if self.value == 4:
            return color.AMBER

    def __str__(self):

        if self.value == 0:
            return "Joker"
        if self.value == 1:
            return "black"
        if self.value == 2:
            return "blue"
        if self.value == 3:
            return "red"
        if self.value == 4:
            return "yellow"

    def __lt__(self, other):
        return self.value < other.value


class Tile:

    Joker = "J"

    def __init__(self, value, color: Color):

        if not (value == self.Joker or 1 <= value <= 13):
            raise ValueError("Value must be between 1 and 13 or Joker")
        if not isinstance(color, Color):
            raise TypeError("Color must be Color(Enum)")

        self.value = value
        self.color = color

    def __str__(self):
        return str(self.value) + str(self.color)

    def __eq__(self, other):
        if not isinstance(other, Tile):
            return False

        return self.color == other.color and self.value == other.value

    def __lt__(self, other):
        if self.value == self.Joker:
            return True
        elif other.value == self.Joker:
            return False
        elif self.value == other.value:
            return self.color < other.color
        return self.value < other.value
