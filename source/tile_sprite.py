import arcade


class TileSprite(arcade.Sprite):
    """ Card sprite """

    def __init__(self, tile_color, value, scale=1):
        """ Card constructor """

        # Attributes for suit and value
        self.tile_color = tile_color
        self.value = value

        # Image to use for the sprite when face up
        self.image_file_name = f"resources/images/test_img.png"

        # Call the parent
        super().__init__(self.image_file_name, scale, hit_box_algorithm="None")


