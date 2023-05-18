import bisect

from .tile import Tile


class Rack:
    """Represents player's rack.

    Rack aggregates tiles currently owned by the player"""

    def __init__(self):
        self.__tiles = []

    def if_tile_on_rack(self, tile: Tile):
        """Check if given tile is on the rack (if is available)"""

        if tile in self.__tiles:
            return True
        return False

    def add_tile(self, tile: Tile):
        """Adds tile to the rack in an ordered way"""

        # Find the index to insert the tile
        index = bisect.bisect_left(self.__tiles, tile)

        # Insert the tile at the determined index
        self.__tiles.insert(index, tile)

    def remove_tile(self, tile: Tile):
        """Remove given tile from the rack"""

        self.__tiles.remove(tile)

    def is_empty(self) -> bool:
        return len(self.__tiles) == 0

    def get_tiles(self):
        return self.__tiles

    def __str__(self):
        res = '['
        for tile in self.__tiles:
            res += tile.__str__()
            res += ", "
        res += ']'
        return res
