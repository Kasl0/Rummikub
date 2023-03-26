from color import Color
from tile import Tile
from random import randint


class TilePool:
    """Pool of tiles which can be drawn by the player"""
    def __init__(self, unavailable_tiles: list[Tile] = []):
        self.__tiles = []
        for color in Color:
            for value in range(1, 14):
                # each tile has to copies in starting pool
                self.__tiles.append(Tile(value, color))
                self.__tiles.append(Tile(value, color))

        for tile in unavailable_tiles:
            self.remove_tile(tile)

    def if_tile_in_pool(self, tile: Tile):
        """Check if given tile is in the pool"""

        for rack_tile in self.__tiles:
            if rack_tile is tile:
                return True
        return False

    def draw_random_tile(self):
        """Draw a random tile from the pool.

        Returns drawn tile or None if there's no more tiles in the pool"""

        if len(self.__tiles) == 0:
            raise Exception("No more tiles in the tile pool")

        rnd_num = randint(0, len(self.__tiles) - 1)
        tile_to_return = self.__tiles[rnd_num]

        self.remove_tile(tile_to_return)
        return tile_to_return

    def remove_tile(self, tile: Tile):
        self.__tiles.remove(tile)
