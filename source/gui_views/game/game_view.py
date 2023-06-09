from enum import Enum
from functools import wraps
from typing import Optional

import arcade.gui

from .game_board import GameBoard
from source.gui_views.view_constants import *
from .game_constants import *
from .game_rack import GameRack
from .game_tile import GameTile

from source.manager.client_actor import ClientActor, ClientActorState
from ..endgame_view import EndgameView


class TakenFrom(Enum):
    BOARD = 1,
    RACK = 2


common_label_style = {
    "x": 0,
    "y": RACK_HEIGHT + GAP / 4,
    "width": RACK_WIDTH,
    "align": "center",
    "font_name": FONT_NAME,
    "font_size": NORMAL_FONT_SIZE
}


def assert_player_is_active(func):
    @wraps(func)
    def wrapper(self, event):
        if self.player.state != ClientActorState.ACTIVE:
            return
        return func(self, event)

    return wrapper


class GameView(arcade.View):

    def __init__(self, client_actor: ClientActor):

        super().__init__()
        self.player = client_actor

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Buttons
        v_box = arcade.gui.UIBoxLayout()

        available_height = RACK_HEIGHT + GAP
        available_width = BOARD_WIDTH - RACK_WIDTH - 2 * GAP

        confirm_button = arcade.gui.UIFlatButton(text="Confirm", width=available_width, height=available_height / 4,
                                                 style=BUTTON_STYLE)
        confirm_button.on_click = self.__on_click_confirm
        v_box.add(confirm_button.with_space_around(bottom=available_height / 16))

        draw_button = arcade.gui.UIFlatButton(text="Draw tile", width=available_width, height=available_height / 4,
                                              style=BUTTON_STYLE)
        draw_button.on_click = self.__on_click_draw
        v_box.add(draw_button.with_space_around(bottom=available_height / 16))

        revert_button = arcade.gui.UIFlatButton(text="Revert changes", width=available_width,
                                                height=available_height / 4,
                                                style=BUTTON_STYLE)
        revert_button.on_click = self.__on_click_revert
        v_box.add(revert_button.with_space_around(bottom=available_height / 16))

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="right",
                align_x=-GAP,
                anchor_y="bottom",
                child=v_box)
        )

        # Gui elements
        self.game_board = GameBoard()
        self.game_rack = GameRack()

        # UI messages and texts
        self.message_label = arcade.gui.UILabel()
        self.manager.add(self.message_label)

        # Held tile
        self.held_tile: Optional[GameTile] = None
        self.held_tile_taken_from = None
        self.held_tile_original_position = None

        self.display_everything()

    def display_everything(self):
        self.game_board.display(self.player.board)
        self.game_rack.display(self.player.rack)

    # Displays error label. If error_text is falsy then display current player's nickname
    def display_error_label(self, error_text: Optional[str]):
        self.manager.remove(self.message_label)

        if error_text:
            self.message_label = arcade.gui.UILabel(text=error_text,
                                                    text_color=ERROR_COLOR, **common_label_style)
            self.manager.add(self.message_label)

        # Display active player nick
        else:
            self.message_label = arcade.gui.UILabel(text="Current player: " + self.player.active_player_nick,
                                                    text_color=MAIN_COLOR, **common_label_style)
            self.manager.add(self.message_label)

    def draw_confirm_error(self, row, column_sequence_start, column_sequence_end, error_message):
        self.display_error_label(error_message)
        self.game_board.mark_wrong_placed(row, column_sequence_start, column_sequence_end)

    def on_draw(self):
        self.clear()

        self.game_board.on_draw()
        self.game_rack.on_draw()

        self.manager.draw()

        if self.held_tile:
            self.held_tile.draw()

    def on_update(self, delta_time: float):
        super().on_update(delta_time)
        if self.player.check_if_should_introduce_changes():
            self.game_board.display(self.player.board)
            print("On_update)")
            self.display_error_label("")
            if self.player.check_if_game_should_end():
                self.__set_endgame_view()

    def __set_endgame_view(self):
        endgame_view = EndgameView("abc")
        self.manager.disable()
        self.manager.clear()
        self.clear()
        self.window.show_view(endgame_view)

    def on_mouse_press(self, x, y, button, key_modifiers):
        """ Called when the user presses a mouse button. """

        # Player can do nothing unless it's his turn
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
                        self.display_error_label("")
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
                                self.display_error_label("")
                            else:
                                self.display_error_label("You cannot take tile from board that is not yours")
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

    @assert_player_is_active
    def __on_click_revert(self, event):
        self.display_error_label("")
        self.game_board.unmark_all_tiles_as_new()
        self.player.handle_revert_changes()
        self.display_everything()

    @assert_player_is_active
    def __on_click_draw(self, event):
        self.display_error_label("")
        self.game_board.unmark_all_tiles_as_new()
        self.player.handle_draw_tile()
        self.display_everything()

    @assert_player_is_active
    def __on_click_confirm(self, event):
        if self.game_board.is_any_tile_new():

            verification_result, row, column_sequence_start, column_sequence_end, error_message = self.player.handle_confirm_changes()
            if verification_result:
                self.display_error_label("")
                self.game_board.unmark_all_tiles_as_new()
            else:
                self.draw_confirm_error(row, column_sequence_start, column_sequence_end, error_message)

        else:
            self.display_error_label("You need to place at least one tile")

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """ User moves mouse """

        # Update the position of the selected card when dragging
        if self.held_tile:
            self.held_tile.update_position(x, y)
