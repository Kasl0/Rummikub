class Vector2d:
    def __init__(self, x: int, y: int):

        if not isinstance(x, int):
            raise TypeError("X must be int")
        if not isinstance(y, int):
            raise TypeError("Y must be int")

        self.x = x
        self.y = y

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    def __eq__(self, other):
        if not isinstance(other, Vector2d):
            return False

        return self.x == other.x and self.y == other.y
