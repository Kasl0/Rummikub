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

    # Returns tile at given position or None if position is not occupied
    def tile_at(self, position: Vector2d) -> Optional[Tile]:

        if not isinstance(position, Vector2d):
            raise TypeError("Position must be Vector2d")
        if not 0 <= position.y < self.rows:
            raise TypeError("Row with such index does not exist")
        if not 0 <= position.x < self.columns:
            raise TypeError("Column with such index " + position.x.__str__() + " does not exist")

        return self.cells[position.y][position.x]

    # Places given tile at given position on the board
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

    # Moves tile on the board
    def move_tile(self, position_from: Vector2d, position_to: Vector2d):

        if not isinstance(position_from, Vector2d):
            raise TypeError("Position_from must be Vector2d")
        if not 0 <= position_from.y < self.rows:
            raise TypeError("Position_from row with such index does not exist")
        if not 0 <= position_from.x < self.columns:
            raise TypeError("Position_from column with such index does not exist")
        if not self.tile_at(position_from):
            raise TypeError("Position_from is not occupied")

        if not isinstance(position_to, Vector2d):
            raise TypeError("Position_to must be Vector2d")
        if not 0 <= position_to.y < self.rows:
            raise TypeError("Position_to row with such index does not exist")
        if not 0 <= position_to.x < self.columns:
            raise TypeError("Position_to column with such index does not exist")
        if self.tile_at(position_to):
            raise TypeError("Position_to is occupied")

        self.cells[position_to.y][position_to.x] = self.cells[position_from.y][position_from.x]
        self.cells[position_from.y][position_from.x] = None

    # Removes tile from given position
    # TO DO: VERIFY WHETHER TILE CAN BE REMOVED - WHETHER TILE IS CURRENT PLAYER TILE
    def remove_tile(self, position: Vector2d):

        if not isinstance(position, Vector2d):
            raise TypeError("Position must be Vector2d")
        if not 0 <= position.y < self.rows:
            raise TypeError("Row with such index does not exist")
        if not 0 <= position.x < self.columns:
            raise TypeError("Column with such index does not exist")
        if not self.tile_at(position):
            raise TypeError("Position is not occupied")

        self.cells[position.y][position.x] = None

    # Verifies the board, checks if every tile is placed correctly
    # Returns (True, None, None, None, None) if everything is placed correctly
    # And (False, row, column_sequence_start, column_sequence_end, error_message) if not
    def verify(self):

        for row in range(self.rows):
            sequence_start = None

            for column in range(self.columns):
                tile = self.tile_at(Vector2d(column, row))

                if isinstance(tile, Tile) and sequence_start is None:
                    sequence_start = column

                elif not isinstance(tile, Tile) and sequence_start is not None:
                    verify_result, error_message = self.verify_sequence(row, sequence_start, column - 1)

                    if not verify_result:
                        return False, row, sequence_start, column - 1, error_message

                    sequence_start = None

            if sequence_start is not None:
                verify_result, error_message = self.verify_sequence(row, sequence_start, self.columns-1)

                if not verify_result:
                    return False, row, sequence_start, self.columns-1, error_message

        return True, None, None, None, None

    def verify_sequence(self, row, start_column, end_column):

        if end_column - start_column < 2:
            return False, "Sequence must be at least 3 tiles long"

        color_sequence = True
        set_sequence = True
        color = self.tile_at(Vector2d(end_column, row)).color
        value = self.tile_at(Vector2d(end_column, row)).value
        colors_in_sequence = {color}

        for i in range(start_column, end_column):
            tile = self.tile_at(Vector2d(i, row))

            if tile.color != color or tile.value + 1 != self.tile_at(Vector2d(i+1, row)).value:
                color_sequence = False

            if tile.value != value or tile.color in colors_in_sequence:
                set_sequence = False

            colors_in_sequence.add(tile.color)

        # print(str(row) + " " + str(start_column) + " " + str(end_column))

        if not (color_sequence or set_sequence):
            return False, "Incorrect sequence"
        else:
            return True, None

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
