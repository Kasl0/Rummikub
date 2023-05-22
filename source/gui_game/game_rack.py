from typing import Optional

import arcade.gui

from .game_constants import *
from .game_tile import GameTile
from ..gui_views.view_constants import SCREEN_WIDTH, SCREEN_HEIGHT
from ..logic.vector2d import Vector2d


class GameRack:
    def __init__(self):
        self.objects_to_draw = arcade.ShapeElementList()
        self.rack_tiles = []

    def get_x_y(self, row, column):

        x = MAT_WIDTH * column + MAT_WIDTH / 2
        y = RACK_HEIGHT - (MAT_HEIGHT * row + MAT_HEIGHT / 2)

        return x, y

    def get_column_row(self, x, y) -> Optional[Vector2d]:
        """
            Returns rack column and row over which (x,y) is hovering or None if it is not hovering over the rack.
        """

        if not 0 < x < RACK_WIDTH:
            return None
        if not 0 < y < RACK_HEIGHT:
            return None

        for row in range(RACK_ROW_COUNT):
            for column in range(RACK_COLUMN_COUNT):

                cell_x = MAT_WIDTH * column + MAT_WIDTH / 2
                cell_y = RACK_HEIGHT - (MAT_HEIGHT * row + MAT_HEIGHT / 2)

                if abs(cell_x - x) < MAT_WIDTH / 2 and abs(cell_y - y) < MAT_HEIGHT / 2:
                    return Vector2d(column, row)

        return None

    def get_game_tile(self, x, y) -> Optional[GameTile]:

        for tile in self.rack_tiles:
            if tile.is_hovering(x, y):
                self.rack_tiles.remove(tile)
                return tile

        return None

    def add_game_tile(self, game_tile):
        self.rack_tiles.append(game_tile)

    def display(self, rack):

        self.rack_tiles = []

        # Draw rack background
        rack_background = arcade.create_rectangle_filled(RACK_WIDTH / 2, RACK_HEIGHT / 2, RACK_WIDTH, RACK_HEIGHT, RACK_COLOR)
        self.objects_to_draw.append(rack_background)

        tiles = rack.get_tiles()
        current_tile = 0

        # Display tiles on rack
        for row in range(RACK_ROW_COUNT):
            for column in range(RACK_COLUMN_COUNT):

                x, y = self.get_x_y(row, column)

                if current_tile < len(tiles):

                    tile_sprite = GameTile(tiles[current_tile], x, y)
                    self.rack_tiles.append(tile_sprite)

                    current_tile += 1

                else:
                    return

    def on_draw(self):
        self.objects_to_draw.draw()

        for tile in self.rack_tiles:
            tile.draw()
