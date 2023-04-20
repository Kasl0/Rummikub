from rack import Rack
from player import Player
from tile_pool import TilePool
from tile import Tile
from board import Board
from input_parser import InputParser


class Game:
    def __init__(self):
        self.board = Board()
        self.tile_pool = TilePool()
        self.rack = Rack()

        self.player = Player(self.board, self.tile_pool, self.rack)
        self.player.draw_starting_tiles()

    def start(self):

        game_loop = True

        print(self.rack)
        print(self.board)
        while game_loop:

            parser = InputParser()

            try:
                # Write "place <position_x> <position_y> <value> <color>" to place a tile
                # Example: "place 5 7 13 blue" places blue 13 at (5,7)
                if parser.is_place():
                    self.player.place_tile(Tile(parser.get_value(), parser.get_color()), parser.get_position())
                    print(self.rack)
                    print(self.board)

                # Write "move <position_from_x> <position_from_y> <position_to_x> <position_to_y>" to move a tile
                if parser.is_move():
                    self.board.move_tile(parser.get_position(), parser.get_position2())
                    print(self.rack)
                    print(self.board)

                # Write "remove <position_x> <position_y>" to take the tile off the board and add it to the rack
                if parser.is_remove():
                    self.player.take_tile_off_board(parser.get_position())
                    print(self.rack)
                    print(self.board)

                #  Write "draw" to draw new tile from pool of available tiles
                if parser.is_draw():
                    self.player.draw_tile()
                    print(self.rack)
                    print(self.board)

                # Write "verify" to confirm your placement and verify moves
                elif parser.is_verify():
                    print(self.board.verify())

                # Write "exit" to end game loop
                elif parser.is_exit():
                    game_loop = False

                else:
                    print("Unknown command")
            except Exception as e:
                print(e)
