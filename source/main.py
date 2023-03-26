from color import Color
from game import Game
from tile import Tile


def main():
    # for testing purposes
    player_tiles = [Tile(1, Color.Red), Tile(2, Color.Red), Tile(3, Color.Red),
                    Tile(7, Color.Blue), Tile(7, Color.Black), Tile(7, Color.Red), Tile(7, Color.Yellow)]

    game = Game(player_tiles, player_tiles)
    game.start()


if __name__ == '__main__':
    main()
