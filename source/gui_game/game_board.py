from typing import Optional

import arcade.gui

from .game_constants import *
from .game_tile import GameTile
from ..gui_views.view_constants import SCREEN_WIDTH, SCREEN_HEIGHT
from ..logic.vector2d import Vector2d


class GameBoard:
    def __init__(self):
        self.objects_to_draw = arcade.ShapeElementList()
        self.board_tiles = []

    def get_x_y(self, row, column):

        x = MAT_WIDTH * column + MAT_WIDTH / 2
        y = SCREEN_HEIGHT - (MAT_HEIGHT * row + MAT_HEIGHT / 2)

        return x, y

    def get_column_row(self, x, y) -> Optional[Vector2d]:
        """
            Returns board column and row over which (x,y) is hovering or None if it is not hovering over the board.
        """

        if not 0 < x < BOARD_WIDTH:
            return None
        if not RACK_HEIGHT + GAP < y < SCREEN_HEIGHT:
            return None

        for row in range(BOARD_ROW_COUNT):
            for column in range(BOARD_COLUMN_COUNT):

                cell_x = MAT_WIDTH * column + MAT_WIDTH / 2
                cell_y = SCREEN_HEIGHT - (MAT_HEIGHT * row + MAT_HEIGHT / 2)

                if abs(cell_x - x) < MAT_WIDTH / 2 and abs(cell_y - y) < MAT_HEIGHT / 2:
                    return Vector2d(column, row)

        return None

    def get_game_tile(self, x, y) -> Optional[GameTile]:

        for tile in self.board_tiles:
            if tile.is_hovering(x, y):
                self.board_tiles.remove(tile)
                return tile

        return None

    def add_game_tile(self, game_tile):
        self.board_tiles.append(game_tile)

    def display(self, board):

        self.board_tiles = []

        # Draw board grid
        board_grid = arcade.create_rectangle_filled(BOARD_WIDTH / 2, RACK_HEIGHT + GAP + BOARD_HEIGHT / 2, BOARD_WIDTH, BOARD_HEIGHT, BOARD_GRID_COLOR)
        self.objects_to_draw.append(board_grid)

        # Display tiles on board or empty space with background color
        for row in range(BOARD_ROW_COUNT):
            for column in range(BOARD_COLUMN_COUNT):

                x, y = self.get_x_y(row, column)

                tile = board.tile_at(Vector2d(column, row))

                current_cell = arcade.create_rectangle_filled(x, y, TILE_WIDTH, TILE_HEIGHT, BOARD_BACKGROUND_COLOR)
                self.objects_to_draw.append(current_cell)

                if tile:
                    game_tile = GameTile(tile, x, y)
                    self.board_tiles.append(game_tile)

    def mark_wrong_placed(self, row, column_sequence_start, column_sequence_end):
        for column in range(column_sequence_start, column_sequence_end+1):
            x, y = self.get_x_y(row, column)

            for tile in self.board_tiles:
                if tile.is_hovering(x, y):
                    tile.mark_wrong_placed()

    def on_draw(self):
        self.objects_to_draw.draw()

        for tile in self.board_tiles:
            tile.draw()
