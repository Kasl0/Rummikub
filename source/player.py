from board import Board
from rack import Rack
from tile_pool import TilePool
from tile import Tile
from vector2d import Vector2d


class Player:
    """Represents the player

    Interacts with board, has his own rack and can draw tiles from pool of available tiles
    """
    def __init__(self, board: Board, tile_pool: TilePool, rack: Rack):
        self.board = board
        self.rack = rack
        self.tile_pool = tile_pool

    def draw_tile(self):
        """Draw random tile from the pool of available tile"""

        drawn_tile = self.tile_pool.draw_random_tile()
        self.rack.add_tile(drawn_tile)

    def place_tile(self, tile: Tile, position: Vector2d):
        """Place given tile on given position at the board"""

        if not self.rack.if_tile_on_rack(tile):
            raise ValueError("Player doesn't have tile " + tile.__str__() + " on his rack")

        self.board.place_tile(tile, position)

        self.rack.remove_tile(tile)

    def take_tile_off_board(self, position: Vector2d):
        """Take tile off the board and add it to player's rack"""

        tile = self.board.take_tile_off(position)
        if tile is not None:
            self.rack.add_tile(tile)

    def draw_starting_tiles(self):
        for i in range(14):
            self.draw_tile()
