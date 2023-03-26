from board import Board
from rack import Rack
from tile_pool import TilePool
from tile import Tile
from vector2d import Vector2d


class Player:
    def __init__(self, board: Board, tile_pool: TilePool, rack: Rack):
        self.board = board
        self.rack = rack
        self.tile_pool = tile_pool

    # Draw random tile from the pool of available tiles
    def draw_tile(self):
        drawn_tile = self.tile_pool.draw_random_tile()
        self.rack.add_tile(drawn_tile)

    # Place given tile on given position at the board
    def place_tile(self, tile: Tile, position: Vector2d):
        if not self.rack.if_tile_on_rack(tile):
            raise Exception("Player doesn't have tile " + tile.__str__() + " on his rack")

        try:
            self.board.place_tile(tile, position)
        except:
            raise Exception("Couldn't place tile " + tile.__str__() +
                            " on position " + position.__str__() +
                            " on the board")

        self.rack.remove_tile(tile)

    # Take tile off the board and add it to player's rack
    def take_tile_off_board(self, position: Vector2d):
        tile = self.board.take_tile_off(position)
        if tile is not None:
            self.rack.add_tile(tile)
