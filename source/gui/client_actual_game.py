from enum import Enum
from typing import List, Optional, Tuple

import arcade
import arcade.gui

from .game_button import GameButton
from .game_constants import *
from .tile_sprite import TileSprite

from ..logic.vector2d import Vector2d
from ..manager.client_actor import ClientActor, ClientActorState


class TakenFrom(Enum):
    BOARD = 1,
    RACK = 2


class ClientActualGame(arcade.View):

    def __init__(self, client_actor: ClientActor):

        super().__init__()
        self.player = client_actor

        self.gui = arcade.ShapeElementList()
        self.confirm_button: Optional[GameButton] = None
        self.draw_button: Optional[GameButton] = None
        self.revert_button: Optional[GameButton] = None

        # Get window dimensions
        self.screen_width, self.screen_height = self.window.get_size()

        self.tile_list: List[TileSprite] = []
        self.held_tile: Optional[TileSprite] = None
        self.held_tile_original_position: Optional[Tuple[float, float]] = None

        self.display_everything()

    def display_everything(self):
        self.gui = arcade.ShapeElementList()
        self.tile_list = []

        self.display_board()
        self.display_rack()
        self.display_buttons()
        # TODO: Display somehow who is an active player (whose turn it is)

    def display_board(self):

        # Draw board grid
        board_grid = arcade.create_rectangle_filled(BOARD_WIDTH / 2,
                                                    self.screen_height - BOARD_HEIGHT / 2,
                                                    BOARD_WIDTH,
                                                    BOARD_HEIGHT,
                                                    BOARD_GRID_COLOR)
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

    def display_rack(self):

        # Draw rack background
        rack_background = arcade.create_rectangle_filled(RACK_WIDTH / 2,
                                                         RACK_HEIGHT / 2,
                                                         RACK_WIDTH,
                                                         RACK_HEIGHT,
                                                         RACK_COLOR)
        self.gui.append(rack_background)

        tiles = self.player.rack.get_tiles()
        current_tile = 0

        # Display tiles on rack
        for row in range(RACK_ROW_COUNT):
            for column in range(RACK_COLUMN_COUNT):

                x = MAT_WIDTH * column + MAT_WIDTH / 2
                y = RACK_HEIGHT - (MAT_HEIGHT * row + MAT_HEIGHT / 2)

                if current_tile < len(tiles):
                    current_cell = TileSprite(tiles[current_tile], x, y)
                    current_tile += 1

                    self.tile_list.append(current_cell)

    def display_buttons(self):

        button_width = 200
        self.confirm_button = GameButton(RACK_WIDTH + GAP + button_width / 2,
                                         RACK_HEIGHT * 5/5,
                                         button_width,
                                         RACK_HEIGHT * 1/4,
                                         "Confirm")
        self.draw_button = GameButton(RACK_WIDTH + GAP + button_width / 2,
                                      RACK_HEIGHT * 3/5,
                                      button_width,
                                      RACK_HEIGHT * 1/4,
                                      "Draw tile")

        self.revert_button = GameButton(RACK_WIDTH + GAP + button_width / 2,
                                        RACK_HEIGHT * 1/5,
                                        button_width,
                                        RACK_HEIGHT * 1/4,
                                        "Revert changes")

    def board_is_hovering(self, x, y) -> Optional[Vector2d]:
        """
            Checks if (x,y) is hovering over the board.
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

    def rack_is_hovering(self, x, y) -> bool:
        if not 0 < x < RACK_WIDTH:
            return False
        if not 0 < y < RACK_HEIGHT:
            return False
        return True

    def on_draw(self):
        arcade.start_render()

        self.gui.draw()

        self.confirm_button.draw()
        self.draw_button.draw()
        self.revert_button.draw()

        for tile in self.tile_list:
            tile.draw()

        arcade.finish_render()

    def on_update(self, delta_time: float):
        super().on_update(delta_time)
        if self.player.check_if_should_introduce_changes():
            self.display_everything()

    def on_mouse_press(self, x, y, button, key_modifiers):
        """ Called when the user presses a mouse button. """

        # player can do nothing unless it's his turn
        if self.player.state != ClientActorState.ACTIVE:
            return

        # Check if the mouse press is on a card
        for tile in self.tile_list:
            if tile.is_hovering(x, y):
                tile.start_dragging()
                self.held_tile = tile
                self.held_tile_original_position = (tile.x, tile.y)
                break

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        """ Called when the user presses a mouse button. """

        # can do nothing unless it's his turn
        if self.player.state != ClientActorState.ACTIVE:
            return

        # Check if the mouse is on confirm button
        if self.confirm_button.is_mouse_on_button(x, y):
            self.player.handle_confirm_changes()
            self.display_everything()

        # Check if the mouse is on draw button
        if self.draw_button.is_mouse_on_button(x, y):
            self.player.handle_draw_tile()
            self.display_everything()

        # Check if the mouse is on revert button
        if self.revert_button.is_mouse_on_button(x, y):
            self.player.handle_revert_changes()
            self.display_everything()

        # Stop dragging the selected card
        if self.held_tile:

            self.held_tile.stop_dragging()

            start_position = self.board_is_hovering(self.held_tile_original_position[0],
                                                    self.held_tile_original_position[1])
            end_position = self.board_is_hovering(x, y)

            if end_position:
                if start_position:
                    # tile was above board when picked up
                    self.player.handle_board_change_move(start_position, end_position)
                else:
                    # tile had to be on the rack
                    self.player.handle_board_change_place(self.held_tile.tile, end_position)

                self.held_tile.x = MAT_WIDTH * end_position.x + MAT_WIDTH / 2
                self.held_tile.y = self.screen_height - (MAT_HEIGHT * end_position.y + MAT_HEIGHT / 2)

            else:
                # cannot place tile, return it to original position
                x_original, y_original = self.held_tile_original_position
                self.held_tile.x = x_original
                self.held_tile.y = y_original

            self.held_tile = None

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """ User moves mouse """

        # Update the position of the selected card when dragging
        if self.held_tile:
            self.held_tile.update_position(x, y)
