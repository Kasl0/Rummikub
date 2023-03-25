from typing import Optional
from tile import Tile
from vector2d import Vector2d


class Board:
    def __init__(self, rows: int = 8, columns: int = 22):

        if not isinstance(rows, int):
            raise TypeError("Rows must be int")
        if not 1 <= rows <= 15:
            raise TypeError("Rows must be between 1 and 15")
        if not isinstance(columns, int):
            raise TypeError("Columns must be int")
        if not 1 <= columns <= 50:
            raise TypeError("Columns must be between 1 and 50")

        self.rows = rows
        self.columns = columns
        self.cells = [[None for _ in range(columns)] for __ in range(rows)]

    def tile_at(self, position: Vector2d) -> Optional[Tile]:

        if not isinstance(position, Vector2d):
            raise TypeError("Position must be Vector2d")
        if not 0 <= position.y < self.rows:
            raise TypeError("Row with such index does not exist")
        if not 0 <= position.x < self.columns:
            raise TypeError("Column with such index does not exist")

        return self.cells[position.y][position.x]

    def place_tile(self, tile: Tile, position: Vector2d):

        if not isinstance(position, Vector2d):
            raise TypeError("Position must be Vector2d")
        if not 0 <= position.y < self.rows:
            raise TypeError("Row with such index does not exist")
        if not 0 <= position.x < self.columns:
            raise TypeError("Column with such index does not exist")
        if self.tile_at(position):
            raise TypeError("Position is occupied")

        self.cells[position.y][position.x] = tile

    def __str__(self):
        return_string = ""

        for row in range(self.rows):
            for column in range(self.columns):
                tile = self.tile_at(Vector2d(column, row))
                if isinstance(tile, Tile):
                    return_string += str(self.cells[row][column])
                else:
                    return_string += "'"
                return_string += " "
            return_string += "\n"

        return return_string
