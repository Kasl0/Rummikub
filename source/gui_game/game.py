from enum import Enum
from typing import List, Optional, Tuple

import arcade.gui

from .game_board import GameBoard
from .game_button import GameButton
from source.gui_views.view_constants import *
from .game_constants import *
from .game_rack import GameRack
from .game_tile import GameTile

from ..logic.vector2d import Vector2d
from ..manager.client_actor import ClientActor, ClientActorState


class TakenFrom(Enum):
    BOARD = 1,
    RACK = 2


class Game(arcade.View):

    def __init__(self, client_actor: ClientActor):

        super().__init__()
        self.player = client_actor

        # Gui elements
        self.game_board = GameBoard()
        self.game_rack = GameRack()

        # Buttons
        self.confirm_button: Optional[GameButton] = None
        self.draw_button: Optional[GameButton] = None
        self.revert_button: Optional[GameButton] = None

        # Error message
        self.error_message: str = ""

        # Held tile
        self.held_tile: Optional[GameTile] = None
        self.held_tile_taken_from = None
        self.held_tile_original_position = None

        self.display_everything()

    def display_everything(self):

        self.game_board.display(self.player.board)
        self.game_rack.display(self.player.rack)
        self.display_buttons()

        # TODO: Display somehow who is an active player (whose turn it is)

    def display_buttons(self):

        button_width = 200
        self.confirm_button = GameButton(RACK_WIDTH + GAP + button_width / 2,
                                         RACK_HEIGHT * 5 / 5,
                                         button_width,
                                         RACK_HEIGHT * 1 / 4,
                                         "Confirm")
        self.draw_button = GameButton(RACK_WIDTH + GAP + button_width / 2,
                                      RACK_HEIGHT * 3 / 5,
                                      button_width,
                                      RACK_HEIGHT * 1 / 4,
                                      "Draw tile")

        self.revert_button = GameButton(RACK_WIDTH + GAP + button_width / 2,
                                        RACK_HEIGHT * 1 / 5,
                                        button_width,
                                        RACK_HEIGHT * 1 / 4,
                                        "Revert changes")

    def draw_confirm_error(self, row, column_sequence_start, column_sequence_end, error_message):

        self.error_message = error_message
        self.game_board.mark_wrong_placed(row, column_sequence_start, column_sequence_end)

    def on_draw(self):
        arcade.start_render()

        self.game_board.on_draw()
        self.game_rack.on_draw()

        self.confirm_button.draw()
        self.draw_button.draw()
        self.revert_button.draw()

        # Display label for error messages
        if self.error_message:
            arcade.draw_text(text=self.error_message, start_x=RACK_WIDTH/2, start_y=RACK_HEIGHT + GAP/2, anchor_x="center", anchor_y="center", font_name=FONT_NAME, font_size=ERROR_FONT_SIZE, color=ERROR_COLOR)

        if self.held_tile:
            self.held_tile.draw()

        arcade.finish_render()

    def on_update(self, delta_time: float):
        super().on_update(delta_time)
        if self.player.check_if_should_introduce_changes():
            self.game_board.display(self.player.board)

    def on_mouse_press(self, x, y, button, key_modifiers):
        """ Called when the user presses a mouse button. """

        # player can do nothing unless it's his turn
        if self.player.state != ClientActorState.ACTIVE:
            return

        # Check if the mouse press is on a board card
        self.held_tile = self.game_board.get_game_tile(x, y)

        if self.held_tile:
            self.held_tile_original_position = (self.held_tile.x, self.held_tile.y)
            self.held_tile_taken_from = TakenFrom.BOARD
            self.held_tile.start_dragging()
            return

        # Check if the mouse press is on a rack card
        self.held_tile = self.game_rack.get_game_tile(x, y)

        if self.held_tile:
            self.held_tile_original_position = (self.held_tile.x, self.held_tile.y)
            self.held_tile_taken_from = TakenFrom.RACK
            self.held_tile.start_dragging()
            return

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        """ Called when the user presses a mouse button. """

        # can do nothing unless it's his turn
        if self.player.state != ClientActorState.ACTIVE:
            return

        if self.held_tile:

            # Stop dragging the selected tile
            self.held_tile.stop_dragging()

            return_to_original = False

            end_position = self.game_board.get_column_row(x, y)

            # Board is final destination
            if end_position:

                # Tile is from rack
                if self.held_tile_taken_from == TakenFrom.RACK:
                    if self.player.board.tile_at(end_position) is None:
                        self.player.handle_board_change_place(self.held_tile.tile, end_position)
                        self.held_tile.x = MAT_WIDTH * end_position.x + MAT_WIDTH / 2
                        self.held_tile.y = SCREEN_HEIGHT - (MAT_HEIGHT * end_position.y + MAT_HEIGHT / 2)
                        self.held_tile.mark_as_new()
                        self.game_board.add_game_tile(self.held_tile)
                    else:
                        return_to_original = True

                # Tile is from board
                elif self.held_tile_taken_from == TakenFrom.BOARD:
                    original_vector2d = self.game_board.get_column_row(*self.held_tile_original_position)
                    if original_vector2d != end_position and self.player.board.tile_at(end_position) is None:
                        self.player.handle_board_change_move(original_vector2d, end_position)
                        self.held_tile.x = MAT_WIDTH * end_position.x + MAT_WIDTH / 2
                        self.held_tile.y = SCREEN_HEIGHT - (MAT_HEIGHT * end_position.y + MAT_HEIGHT / 2)
                        self.game_board.add_game_tile(self.held_tile)
                        self.error_message = ""
                    else:
                        return_to_original = True

                else:
                    raise ValueError("We don't know where tile is from")

            else:

                end_position = self.game_rack.get_column_row(x, y)

                # Rack is final destination
                if end_position:

                    # Tile is from rack
                    if self.held_tile_taken_from == TakenFrom.RACK:
                        if self.game_rack.get_game_tile(x, y, remove=False, over_mat=True) is None:
                            self.held_tile.x = MAT_WIDTH * end_position.x + MAT_WIDTH / 2
                            self.held_tile.y = RACK_HEIGHT - (MAT_HEIGHT * end_position.y + MAT_HEIGHT / 2)
                            self.game_rack.add_game_tile(self.held_tile)
                        else:
                            return_to_original = True

                    # Tile is from board
                    elif self.held_tile_taken_from == TakenFrom.BOARD:
                        original_vector2d = self.game_board.get_column_row(*self.held_tile_original_position)
                        if self.game_rack.get_game_tile(x, y, remove=False, over_mat=True) is None:
                            if self.held_tile.is_new:
                                self.player.handle_board_change_remove(original_vector2d)
                                self.held_tile.x = MAT_WIDTH * end_position.x + MAT_WIDTH / 2
                                self.held_tile.y = RACK_HEIGHT - (MAT_HEIGHT * end_position.y + MAT_HEIGHT / 2)
                                self.game_rack.add_game_tile(self.held_tile)
                                self.error_message = ""
                            else:
                                self.error_message = "You cannot take tile from board that is not yours"
                                return_to_original = True
                        else:
                            return_to_original = True

                    else:
                        raise ValueError("We don't know where tile is from")

                # No destination, return to original
                else:
                    return_to_original = True

            # cannot place tile, return it to original position
            if return_to_original:

                if self.held_tile_taken_from == TakenFrom.RACK:
                    self.held_tile.x, self.held_tile.y = self.held_tile_original_position
                    self.game_rack.add_game_tile(self.held_tile)

                elif self.held_tile_taken_from == TakenFrom.BOARD:
                    self.held_tile.x, self.held_tile.y = self.held_tile_original_position
                    self.game_board.add_game_tile(self.held_tile)

                else:
                    raise ValueError("We don't know where tile is from")

            self.held_tile_taken_from = None
            self.held_tile = None

        # Check if the mouse is on confirm button
        elif self.confirm_button.is_mouse_on_button(x, y):

            if self.game_board.is_any_tile_new():

                verification_result, row, column_sequence_start, column_sequence_end, error_message = self.player.handle_confirm_changes()
                if verification_result:
                    self.error_message = ""
                    self.game_board.unmark_all_tiles_as_new()
                else:
                    self.draw_confirm_error(row, column_sequence_start, column_sequence_end, error_message)

            else:
                self.error_message = "You need to place at least one tile"

        # Check if the mouse is on draw button
        elif self.draw_button.is_mouse_on_button(x, y):
            self.error_message = ""
            self.game_board.unmark_all_tiles_as_new()
            self.player.handle_draw_tile()
            self.display_everything()

        # Check if the mouse is on revert button
        elif self.revert_button.is_mouse_on_button(x, y):
            self.error_message = ""
            self.game_board.unmark_all_tiles_as_new()
            self.player.handle_revert_changes()
            self.display_everything()

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """ User moves mouse """

        # Update the position of the selected card when dragging
        if self.held_tile:
            self.held_tile.update_position(x, y)
