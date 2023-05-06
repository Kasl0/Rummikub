import arcade

from ..logic.tile import Tile


class TileSprite(arcade.SpriteSolidColor):
    """ Card sprite """

    def __init__(self, tile):
        """ Card constructor """

        self.tile = tile

        # Call the parent
        super().__init__()


