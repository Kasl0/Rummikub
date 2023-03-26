from board import Board
from vector2d import Vector2d
from tile import Tile


class Rack:
    def __init__(self, starting_tiles: list[Tile] = []):
        self.tiles = starting_tiles

    # check if given tile is on the rack (if is available)
    def if_tile_on_rack(self, tile: Tile):
        if tile in self.tiles:
            return True
        return False

    def add_tile(self, tile: Tile):
        self.tiles.append(tile)

    def remove_tile(self, tile: Tile):
        self.tiles.remove(tile)

    def __str__(self):
        res = '['
        for tile in self.tiles:
            res += tile.__str__()
            res += ", "
        res += ']'
        return res
