from color import Color
from tile import Tile
from random import randint


class TilePool:
    """Pool of tiles which can be drawn by the player"""
    def __init__(self):
        self.tiles = []
        for color in Color:
            for value in range(1, 14):
                # each tile has to copies in starting pool
                self.tiles.append(Tile(value, color))
                self.tiles.append(Tile(value, color))

    def if_tile_in_pool(self, tile: Tile):
        """Check if given tile is in the pool"""

        for rack_tile in self.tiles:
            if rack_tile is tile:
                return True
        return False

    def draw_random_tile(self):
        """Draw a random tile from the pool.

        Returns drawn tile or None if there's no more tiles in the pool"""

        if len(self.tiles) == 0:
            raise Exception("No more tiles in the tile pool")

        rnd_num = randint(0, len(self.tiles) - 1)
        tile_to_return = self.tiles[rnd_num]

        self.remove_tile(tile_to_return)
        return tile_to_return

    def remove_tile(self, tile: Tile):
        self.tiles.remove(tile)
