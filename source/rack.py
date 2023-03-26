from board import Board
from vector2d import Vector2d
from tile import Tile


class Rack:
    """Respresents player's rack.

    Rack aggregates tiles currently owned by the player"""
    def __init__(self, starting_tiles: list[Tile] = []):
        self.__tiles = starting_tiles

    def if_tile_on_rack(self, tile: Tile):
        """Check if given tile is on the rack (if is available)"""

        if tile in self.__tiles:
            return True
        return False

    def add_tile(self, tile: Tile):
        self.__tiles.append(tile)

    def remove_tile(self, tile: Tile):
        """Remove given tile from the rack"""

        self.__tiles.remove(tile)

    def __str__(self):
        res = '['
        for tile in self.__tiles:
            res += tile.__str__()
            res += ", "
        res += ']'
        return res
