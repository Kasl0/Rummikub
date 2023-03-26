from tile import Tile
from board import Board
from input_parser import InputParser
from color import Color
from vector2d import Vector2d


class Game:
    def __init__(self):
        self.board = Board()

        # For testing purposes:
        self.board.place_tile(Tile(1, Color.Red), Vector2d(0, 0))
        self.board.place_tile(Tile(2, Color.Red), Vector2d(1, 0))
        self.board.place_tile(Tile(3, Color.Red), Vector2d(2, 0))

        self.board.place_tile(Tile(7, Color.Red), Vector2d(19, 1))
        self.board.place_tile(Tile(7, Color.Blue), Vector2d(20, 1))
        self.board.place_tile(Tile(7, Color.Black), Vector2d(21, 1))
        #

    def start(self):

        game_loop = True

        while game_loop:

            parser = InputParser()

            # Write "place <position_x> <position_y> <value> <color>" to place a tile
            # Example: "place 5 7 13 blue" places blue 13 at (5,7)
            if parser.is_place():
                self.board.place_tile(Tile(parser.get_value(), parser.get_color()), parser.get_position())
                print(self.board)

            # Write "move <position_from_x> <position_from_y> <position_to_x> <position_to_y>" to move a tile
            if parser.is_move():
                self.board.move_tile(parser.get_position(), parser.get_position2())
                print(self.board)

            # Write "remove <position_x> <position_y>" to remove a tile
            if parser.is_remove():
                self.board.remove_tile(parser.get_position())
                print(self.board)

            # Write "verify" to confirm your placement and verify moves
            elif parser.is_verify():
                print(self.board.verify())

            # Write "exit" to end game loop
            elif parser.is_exit():
                game_loop = False

            else:
                print("Unknown command")
