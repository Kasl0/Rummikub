from color import Color
from tile import Tile
from random import randint


class TilePool:
    def __init__(self, unavailable_tiles: list[Tile] = []):
        self.tiles = []
        for color in Color:
            for value in range(1, 14):
                # each tile has to copies in starting pool
                self.tiles.append(Tile(value, color))
                self.tiles.append(Tile(value, color))

        for tile in unavailable_tiles:
            self.remove_tile(tile)

    # check if given tile is in the pool
    def if_tile_in_pool(self, tile: Tile):
        for rack_tile in self.tiles:
            if rack_tile is tile:
                return True
        return False

    # draw a random tile from the pool
    def draw_random_tile(self):
        rnd_num = randint(0, len(self.tiles) - 1)
        tile_to_return = self.tiles[rnd_num]

        self.remove_tile(tile_to_return)
        return tile_to_return

    def remove_tile(self, tile: Tile):
        self.tiles.remove(tile)
