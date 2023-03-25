from vector2d import Vector2d
from color import Color
from tile import Tile
from board import Board


class Game:
    def __init__(self):
        self.board = Board()

    def start(self):
        self.board.place_tile(Tile(1, Color.Black), Vector2d(1, 1))
        self.board.place_tile(Tile(8, Color.Red), Vector2d(7, 6))
        self.board.place_tile(Tile(13, Color.Yellow), Vector2d(12, 6))
        self.board.place_tile(Tile(3, Color.Blue), Vector2d(5, 5))

        print(self.board)
