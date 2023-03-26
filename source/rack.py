from board import Board
from vector2d import Vector2d
from tile import Tile


class Rack:
    """Respresents player's rack.

    Rack aggregates tiles currently owned by the player"""
    def __init__(self):
        self.tiles = []

    def if_tile_on_rack(self, tile: Tile):
        """Check if given tile is on the rack (if is available)"""

        if tile in self.tiles:
            return True
        return False

    def add_tile(self, tile: Tile):
        self.tiles.append(tile)

    def remove_tile(self, tile: Tile):
        """Remove given tile from the rack"""

        self.tiles.remove(tile)

    def __str__(self):
        res = '['
        for tile in self.tiles:
            res += tile.__str__()
            res += ", "
        res += ']'
        return res
