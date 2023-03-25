from color import Color


class Tile:
    def __init__(self, value: int, color: Color):

        if not isinstance(value, int):
            raise TypeError("Value must be int")
        if not 1 <= value <= 13:
            raise TypeError("Value must be between 1 and 13")
        if not isinstance(color, Color):
            raise TypeError("Color must be Color(Enum)")

        self.value = value
        self.color = color

    def __str__(self):
        return str(self.color) + str(self.value)
