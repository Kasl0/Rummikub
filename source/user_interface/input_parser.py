from ..logic.vector2d import Vector2d
from ..logic.color import Color


class InputParser:
    """Temporary command line parser.

    No input validation"""

    def __init__(self):
        self.words = input().split()

    def is_place(self):
        return self.words[0] == "place"

    def is_move(self):
        return self.words[0] == "move"

    def is_remove(self):
        return self.words[0] == "remove"

    def is_draw(self):
        return self.words[0] == "draw"

    def is_verify(self):
        return self.words[0] == "verify"

    def is_confirm(self):
        return self.words[0] == "confirm"

    def is_revert(self):
        return self.words[0] == "revert"

    def is_exit(self):
        return self.words[0] == "exit"

    def get_position(self):
        x = int(self.words[1])
        y = int(self.words[2])

        return Vector2d(x, y)

    def get_position2(self):
        x = int(self.words[3])
        y = int(self.words[4])

        return Vector2d(x, y)

    def get_value(self):
        value = int(self.words[3])

        if not 1 <= value <= 13:
            raise TypeError("Value must be between 1 and 13")

        return value

    def get_color(self):
        if self.words[4] == "black":
            return Color.Black
        if self.words[4] == "blue":
            return Color.Blue
        if self.words[4] == "red":
            return Color.Red
        if self.words[4] == "yellow":
            return Color.Yellow
