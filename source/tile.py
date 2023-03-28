from color import Color


class Tile:
    def __init__(self, value: int, color: Color):

        if not isinstance(value, int):
            raise TypeError("Value must be int")
        if not 1 <= value <= 13:
            raise ValueError("Value must be between 1 and 13")
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
