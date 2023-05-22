from typing import Optional

from .tile import Tile, Color
from .vector2d import Vector2d


class Board:
    """Represents a board the game is played on. Stores placed tiles and verifies if tiles placement is correct
    """
    def __init__(self, rows: int = 8, columns: int = 22):

        if not isinstance(rows, int):
            raise TypeError("Rows must be int")
        if not 1 <= rows <= 15:
            raise ValueError("Rows must be between 1 and 15")
        if not isinstance(columns, int):
            raise TypeError("Columns must be int")
        if not 1 <= columns <= 50:
            raise ValueError("Columns must be between 1 and 50")

        self._rows = rows
        self._columns = columns
        self._cells = [[None for _ in range(columns)] for __ in range(rows)]

    def tile_at(self, position: Vector2d) -> Optional[Tile]:
        """Returns tile at given position or None if position is not occupied"""

        if not isinstance(position, Vector2d):
            raise TypeError("Position must be Vector2d")
        if not 0 <= position.y < self._rows:
            raise ValueError("Row with such index does not exist")
        if not 0 <= position.x < self._columns:
            raise ValueError("Column with such index " + position.x.__str__() + " does not exist")

        return self._cells[position.y][position.x]

    def place_tile(self, tile: Tile, position: Vector2d):
        """Places given tile at given position on the board"""

        if not isinstance(position, Vector2d):
            raise TypeError("Position must be Vector2d")
        if not 0 <= position.y < self._rows:
            raise ValueError("Row with such index does not exist")
        if not 0 <= position.x < self._columns:
            raise ValueError("Column with such index does not exist")
        if self.tile_at(position):
            raise ValueError("Position is occupied")

        self._cells[position.y][position.x] = tile

    def move_tile(self, position_from: Vector2d, position_to: Vector2d):
        """Moves tile on the board"""

        if not isinstance(position_from, Vector2d):
            raise TypeError("Position_from must be Vector2d")
        if not 0 <= position_from.y < self._rows:
            raise ValueError("Position_from row with such index does not exist")
        if not 0 <= position_from.x < self._columns:
            raise ValueError("Position_from column with such index does not exist")
        if not self.tile_at(position_from):
            raise ValueError("Position_from is not occupied")

        if not isinstance(position_to, Vector2d):
            raise TypeError("Position_to must be Vector2d")
        if not 0 <= position_to.y < self._rows:
            raise ValueError("Position_to row with such index does not exist")
        if not 0 <= position_to.x < self._columns:
            raise ValueError("Position_to column with such index does not exist")
        if self.tile_at(position_to):
            raise ValueError("Position_to is occupied")

        self._cells[position_to.y][position_to.x] = self._cells[position_from.y][position_from.x]
        self._cells[position_from.y][position_from.x] = None

    def take_tile_off(self, position: Vector2d):
        """Take tile off the board and return it"""

        tile = self.tile_at(position)
        if tile is None:
            return None

        self.__remove_tile(position)
        return tile

    def __remove_tile(self, position: Vector2d):
        """Removes tile from given position"""

        if not isinstance(position, Vector2d):
            raise TypeError("Position must be Vector2d")
        if not 0 <= position.y < self._rows:
            raise ValueError("Row with such index does not exist")
        if not 0 <= position.x < self._columns:
            raise ValueError("Column with such index does not exist")
        if not self.tile_at(position):
            raise ValueError("Position is not occupied")

        self._cells[position.y][position.x] = None

    def verify(self):
        """Verifies the board, checks if every tile is placed correctly.

        Returns:
            (True, None, None, None, None) if everything is placed correctly. If not, returns
            (False, row, column_sequence_start, column_sequence_end, error_message)"""

        for row in range(self._rows):
            sequence_start = None

            for column in range(self._columns):
                tile = self.tile_at(Vector2d(column, row))

                if isinstance(tile, Tile) and sequence_start is None:
                    sequence_start = column

                elif not isinstance(tile, Tile) and sequence_start is not None:
                    verification_result, error_message = self.__verify_sequence(row, sequence_start, column - 1)

                    if not verification_result:
                        return False, row, sequence_start, column - 1, error_message

                    sequence_start = None

            if sequence_start is not None:
                verification_result, error_message = self.__verify_sequence(row, sequence_start, self._columns - 1)

                if not verification_result:
                    return False, row, sequence_start, self._columns - 1, error_message

        return True, None, None, None, None

    def __verify_sequence(self, row, start_column, end_column):

        if end_column - start_column < 2:
            return False, "Sequence must be at least 3 tiles long"

        color_sequence = True
        set_sequence = True

        if self.tile_at(Vector2d(start_column, row)).value == Tile.Joker and self.tile_at(Vector2d(start_column+1, row)).value == 1:
            color_sequence = False

        if self.tile_at(Vector2d(end_column, row)).value == Tile.Joker and self.tile_at(Vector2d(end_column-1, row)).value == 13:
            color_sequence = False

        color = None
        value = None
        colors_in_sequence = None

        for i in range(end_column, start_column, -1):
            tile = self.tile_at(Vector2d(i, row))
            if tile.value != Tile.Joker:
                color = tile.color
                value = tile.value
                colors_in_sequence = {color}
                end_column = i
                break

        for i in range(start_column, end_column):
            tile = self.tile_at(Vector2d(i, row))

            if tile.value != Tile.Joker and tile.color != Color.Joker:
                if tile.color != color or (self.tile_at(Vector2d(i+1, row)).value != Tile.Joker and tile.value + 1 != self.tile_at(Vector2d(i+1, row)).value):
                    color_sequence = False

                if tile.value != value or tile.color in colors_in_sequence:
                    set_sequence = False

                colors_in_sequence.add(tile.color)

            else:
                if i != start_column:
                    if self.tile_at(Vector2d(i-1, row)).value + 2 != self.tile_at(Vector2d(i+1, row)).value:
                        color_sequence = False

        if not (color_sequence or set_sequence):
            return False, "Incorrect sequence"
        else:
            return True, None

    def __str__(self):
        return_string = ""

        for row in range(self._rows):
            for column in range(self._columns):
                tile = self.tile_at(Vector2d(column, row))
                if isinstance(tile, Tile):
                    return_string += str(self._cells[row][column])
                else:
                    return_string += "'"
                return_string += " "
            return_string += "\n"

        return return_string
