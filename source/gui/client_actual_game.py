import arcade
import arcade.gui

# Constants for sizing
TILE_SCALE = 0.6

# How big are the tiles
TILE_WIDTH = int(100 * TILE_SCALE)
TILE_HEIGHT = int(160 * TILE_SCALE)

# How big is the board we'll place the tiles on
MAT_PERCENT_OVERSIZE = 1.25
MAT_HEIGHT = int(TILE_HEIGHT * MAT_PERCENT_OVERSIZE)
MAT_WIDTH = int(TILE_WIDTH * MAT_PERCENT_OVERSIZE)

# How much space do we leave as a gap between the tiles
# Done as a percent of the tile size.
VERTICAL_MARGIN_PERCENT = 0.10
HORIZONTAL_MARGIN_PERCENT = 0.10

# The Y of the bottom row (2 piles)
BOTTOM_Y = MAT_HEIGHT / 2 + MAT_HEIGHT * VERTICAL_MARGIN_PERCENT

# The X of where to start putting things on the left side
START_X = MAT_WIDTH / 2 + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT


class ClientActualGame:

    def __init__(self, app, rack):
        self.app = app
        self.rack = rack
        self.tile_list = arcade.SpriteList()

        self.held_tile = None
        self.held_tile_original_position = None

        self.app.add_draw_observer(self)
        self.display_rack()

    def display_rack(self):
        for i, tile in enumerate(self.rack.get_tiles()):
            #tile_sprite = arcade.SpriteSolidColor(width=TILE_WIDTH, height=TILE_HEIGHT, color=arcade.color.WHITE_SMOKE)
            tile_sprite = arcade.Sprite("C:/Users/Kaslo/Desktop/GitHub/Rummikub/resources/images/tile.png", TILE_SCALE, hit_box_algorithm="None")
            tile_sprite.position = START_X + i * MAT_WIDTH, BOTTOM_Y

            self.tile_list.append(tile_sprite)

    def pull_to_top(self, card: arcade.Sprite):
        """ Pull card to top of rendering order (last to render, looks on-top) """

        # Remove, and append to the end
        self.tile_list.remove(card)
        self.tile_list.append(card)

    def on_draw(self):
        self.app.clear()
        # arcade.start_render()
        self.tile_list.draw()

    def on_mouse_press(self, x, y, button, key_modifiers):
        """ Called when the user presses a mouse button. """

        # Get list of cards we've clicked on
        tiles = arcade.get_sprites_at_point((x, y), self.tile_list)

        # Have we clicked on some tiles?
        if len(tiles) > 0:
            # All other cases, grab the face-up card we are clicking on
            self.held_tile = tiles[0]
            # Save the position
            self.held_tile_original_position = self.held_tile.position
            # Put on top in drawing order
            self.pull_to_top(self.held_tile)

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        """ Called when the user presses a mouse button. """

        # if we don't have any cards, who cares
        if self.held_tile is None:
            return

        # we are no longer holding cards
        self.held_tile = None


        # TODO: temporarily we hardcode actiones that should be performed when dropping card
        #  When the window becomes more functional, these handlers will be called depending on situation

        # if we want to make some action (draw a tile, place / move / remove tile, revert changes, end our turn)
        # just use one of client_actor's handlers
        # self.client_actor.handle_draw_tile()

        # TODO: After calling "handle_draw_card" and "handle_confirm_changes" (if it succeeds), an "enter_passive_state"
        #  is automatically called, so we can listen to the active player's changes.
        #  But how will we be able to update the window then? For now it just freezes (because we wait for messages
        #  inside arcade loop, which is supposed to refresh window) and it's not good :(
        #  (should we create separate thread?)
        #  And how should the window even know, that it should refresh (because the state of the board changed)?

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """ User moves mouse """

        if self.held_tile is not None:
            self.held_tile.center_x += dx
            self.held_tile.center_y += dy
