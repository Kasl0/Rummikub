import arcade

from source.logic.tile import Color
from source.manager.client_actor import ClientActor
from source.tile_sprite import TileSprite

# Screen title and size
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Rummikub"

# Constants for sizing
TILE_SCALE = 0.6

# How big are the tiles?
TILE_WIDTH = 100 * TILE_SCALE
TILE_HEIGHT = 160 * TILE_SCALE

# How big is the board we'll place the tiles on?
MAT_PERCENT_OVERSIZE = 1.25
MAT_HEIGHT = int(TILE_HEIGHT * MAT_PERCENT_OVERSIZE)
MAT_WIDTH = int(TILE_WIDTH * MAT_PERCENT_OVERSIZE)

# How much space do we leave as a gap between the tiles?
# Done as a percent of the tile size.
VERTICAL_MARGIN_PERCENT = 0.10
HORIZONTAL_MARGIN_PERCENT = 0.10

# The Y of the bottom row (2 piles)
BOTTOM_Y = MAT_HEIGHT / 2 + MAT_HEIGHT * VERTICAL_MARGIN_PERCENT

# The X of where to start putting things on the left side
START_X = MAT_WIDTH / 2 + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT

# Card constants
TILE_VALUES = [i for i in range(1, 14)]
TILE_COLORS = [Color.Red, Color.Blue, Color.Black, Color.Yellow]


class ClientWindow(arcade.Window):
    """ Main application class. """

    def __init__(self, client_actor: ClientActor):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # for logic
        self.client_actor = client_actor

        # for tile dragging and gui
        self.tile_list = None
        self.held_tile = None

        # Original location of a tile we are dragging with the mouse in case they have to go back.
        self.held_tile_original_position = None
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """

        # List of cards we are dragging with the mouse
        self.held_tile = None

        # Original location of cards we are dragging with the mouse in case
        # they have to go back.
        self.held_tile_original_position = None

        # Sprite list with all the cards, no matter what pile they are in.
        self.tile_list = arcade.SpriteList()

        # Create every card
        for tile_color in TILE_COLORS:
            for tile_value in TILE_VALUES:
                tile = TileSprite(tile_color, tile_value, TILE_SCALE)
                tile.position = START_X, BOTTOM_Y
                self.tile_list.append(tile)

        self.client_actor.enter_passive_state()

    def pull_to_top(self, card: arcade.Sprite):
        """ Pull card to top of rendering order (last to render, looks on-top) """

        # Remove, and append to the end
        self.tile_list.remove(card)
        self.tile_list.append(card)

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        self.clear()

        # Draw the cards
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

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
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
        self.client_actor.handle_draw_tile()

        # TODO: After calling "handle_draw_card" and "handle_confirm_changes" (if it succeeds) an "enter_passive_state"
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
