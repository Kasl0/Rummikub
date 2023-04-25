import random

from color import Color
from tile import Tile
from random import randint


class TilePool:
    """Pool of tiles which can be drawn by the player"""

    def __init__(self):
        self.__tiles = []

        for color in Color:
            for value in range(1, 14):
                # each tile has to copies in starting pool
                self.__tiles.append(Tile(value, color))
                self.__tiles.append(Tile(value, color))

        random.shuffle(self.__tiles)
        print(self)


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
            return None

        return self.__tiles.pop()

    def remove_tile(self, tile: Tile):
        self.__tiles.remove(tile)

    def __str__(self):
        res = "["

        for tile in self.__tiles:
            res += tile.__str__() + ", "

        res += "]"

        return res
