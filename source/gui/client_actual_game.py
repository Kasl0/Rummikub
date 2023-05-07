import arcade
import arcade.gui

from .game_constants import *
from .tile_sprite import TileSprite, draw_rounded_rectangle_filled
from ..logic.vector2d import Vector2d


class ClientActualGame(arcade.View):

    def __init__(self, client_actor):

        super().__init__()
        self.player = client_actor

        self.gui = None

        self.tile_list = []
        self.held_tile = None
        self.held_tile_original_position = None

        self.display_board()
        self.display_rack()

    def display_board(self):

        # Get window dimensions
        screen_width, screen_height = self.window.get_size()

        self.gui = arcade.ShapeElementList()

        # Draw board grid
        board_grid = arcade.create_rectangle_filled(BOARD_WIDTH / 2, screen_height - BOARD_HEIGHT / 2, BOARD_WIDTH, BOARD_HEIGHT, BOARD_GRID_COLOR)
        self.gui.append(board_grid)

        # Display tiles on board or empty space with background color
        for row in range(BOARD_ROW_COUNT):
            for column in range(BOARD_COLUMN_COUNT):

                x = MAT_WIDTH * column + MAT_WIDTH / 2
                y = screen_height - (MAT_HEIGHT * row + MAT_HEIGHT / 2)

                tile = self.player.board.tile_at(Vector2d(column, row))

                if tile:
                    current_cell = TileSprite(tile, x, y)
                    self.tile_list.append(current_cell)
                else:
                    current_cell = arcade.create_rectangle_filled(x, y, TILE_WIDTH, TILE_HEIGHT, BOARD_BACKGROUND_COLOR)
                    self.gui.append(current_cell)

    def display_rack(self):

        # Draw rack background
        rack_background = arcade.create_rectangle_filled(RACK_WIDTH / 2, RACK_HEIGHT / 2, RACK_WIDTH, RACK_HEIGHT, RACK_COLOR)
        self.gui.append(rack_background)

        tiles = self.player.rack.get_tiles()
        current_tile = 0

        # Display tiles on rack
        for row in range(RACK_ROW_COUNT):
            for column in range(RACK_COLUMN_COUNT):

                x = MAT_WIDTH * column + MAT_WIDTH / 2
                y = MAT_HEIGHT * row + MAT_HEIGHT / 2

                if current_tile < len(tiles):
                    current_cell = TileSprite(tiles[current_tile], x, y)
                    current_tile += 1

                    self.tile_list.append(current_cell)

    def pull_to_top(self, card):
        """ Pull card to top of rendering order (last to render, looks on-top) """

        # Remove, and append to the end
        self.tile_list.remove(card)
        self.tile_list.append(card)

    def on_draw(self):
        arcade.start_render()

        self.gui.draw()

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
