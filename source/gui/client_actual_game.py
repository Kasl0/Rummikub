import arcade
import arcade.gui

from .game_constants import *
from .tile_sprite import TileSprite


class ClientActualGame(arcade.View):

    def __init__(self, rack):
        super().__init__()
        self.rack = rack
        self.tile_list = []

        self.held_tile = None
        self.held_tile_original_position = None

        self.display_rack()

    def display_rack(self):

        for i, tile in enumerate(self.rack.get_tiles()):
            tile_sprite = TileSprite(tile, START_X + i * MAT_WIDTH, BOTTOM_Y)
            self.tile_list.append(tile_sprite)

    def pull_to_top(self, card):
        """ Pull card to top of rendering order (last to render, looks on-top) """

        # Remove, and append to the end
        self.tile_list.remove(card)
        self.tile_list.append(card)

    def on_draw(self):
        arcade.start_render()

        # Draw the cards
        for card in self.tile_list:
            card.draw()

        arcade.finish_render()

    def on_mouse_press(self, x, y, button, key_modifiers):
        """ Called when the user presses a mouse button. """

        # Check if the mouse press is on a card
        for card in self.tile_list:
            if card.is_hovering(x, y):
                card.start_dragging()
                self.held_tile = card
                break

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        """ Called when the user presses a mouse button. """

        # Stop dragging the selected card
        if self.held_tile:
            self.held_tile.stop_dragging()
            self.held_tile = None

        # TODO: temporarily we hardcode actiones that should be performed when dropping card
        #  When the window becomes more functional, these handlers will be called depending on situation

        # if we want to make some action (draw a tile, place / move / remove tile, revert changes, end our turn)
        # just use one of client_actor's handlers
        # self.client_actor.handle_draw_tile()

        # TODO: After calling "handle_draw_card" and "handle_confirm_changes" (if it succeeds), an "enter_passive_state"
        #  is automatically called, so we can listen to the active player's changes.

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """ User moves mouse """

        # Update the position of the selected card when dragging
        if self.held_tile:
            self.held_tile.update_position(x, y)
