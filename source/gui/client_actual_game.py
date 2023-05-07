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

        # Get window dimensions
        self.screen_width, self.screen_height = self.window.get_size()

        self.tile_list = []
        self.held_tile = None
        self.held_tile_original_position = None

        self.display_board()
        self.display_rack()

    def display_board(self):

        self.gui = arcade.ShapeElementList()

        # Draw board grid
        board_grid = arcade.create_rectangle_filled(BOARD_WIDTH / 2, self.screen_height - BOARD_HEIGHT / 2, BOARD_WIDTH, BOARD_HEIGHT, BOARD_GRID_COLOR)
        self.gui.append(board_grid)

        # Display tiles on board or empty space with background color
        for row in range(BOARD_ROW_COUNT):
            for column in range(BOARD_COLUMN_COUNT):

                x = MAT_WIDTH * column + MAT_WIDTH / 2
                y = self.screen_height - (MAT_HEIGHT * row + MAT_HEIGHT / 2)

                tile = self.player.board.tile_at(Vector2d(column, row))

                if tile:
                    current_cell = TileSprite(tile, x, y)
                    self.tile_list.append(current_cell)
                else:
                    current_cell = arcade.create_rectangle_filled(x, y, TILE_WIDTH, TILE_HEIGHT, BOARD_BACKGROUND_COLOR)
                    self.gui.append(current_cell)

    def board_is_hovering(self, x, y):
        """
            Checks if (x,y) is hovering over the board.
            If yes, returns cell position (Vector2d) on the board over which is hovering, else None.
        """

        if not 0 < x < BOARD_WIDTH:
            return None
        if not self.screen_height - BOARD_HEIGHT < y < self.screen_height:
            return None

        for row in range(BOARD_ROW_COUNT):
            for column in range(BOARD_COLUMN_COUNT):

                cell_x = MAT_WIDTH * column + MAT_WIDTH / 2
                cell_y = self.screen_height - (MAT_HEIGHT * row + MAT_HEIGHT / 2)

                if abs(cell_x - x) < MAT_WIDTH / 2 and abs(cell_y - y) < MAT_HEIGHT / 2:
                    return Vector2d(column, row)

        return None

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

        for tile in self.tile_list:
            tile.draw()

        arcade.finish_render()

    def on_mouse_press(self, x, y, button, key_modifiers):
        """ Called when the user presses a mouse button. """

        # Check if the mouse press is on a card
        for tile in self.tile_list:
            if tile.is_hovering(x, y):
                tile.start_dragging()
                self.held_tile = tile
                self.held_tile_original_position = (tile.x, tile.y)
                break

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        """ Called when the user presses a mouse button. """

        # Stop dragging the selected card
        if self.held_tile:

            self.held_tile.stop_dragging()

            position = self.board_is_hovering(x, y)

            if position:
                self.held_tile.x = MAT_WIDTH * position.x + MAT_WIDTH / 2
                self.held_tile.y = self.screen_height - (MAT_HEIGHT * position.y + MAT_HEIGHT / 2)

            else:
                # if cannot place tile, return it to original position
                x_original, y_original = self.held_tile_original_position
                self.held_tile.x = x_original
                self.held_tile.y = y_original

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
