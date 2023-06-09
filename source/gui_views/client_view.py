import re
from typing import Optional

from arcade.gui import UIManager
from keyboard import press, release
from pyautogui import typewrite
from pyperclip import paste
import arcade.gui

from source.gui_views.game.game_view import GameView
from source.logic.board import Board
from source.manager.client_actor import ClientActor
from source.manager.client_game_manager import ClientGameManager
from source.gui_views.view_constants import *


class ClientView(arcade.View):

    def __init__(self):

        super().__init__()
        self.manager = UIManager()
        self.manager.enable()

        self.v_box = arcade.gui.UIBoxLayout()
        self.v_box.align = "left"

        self.client_game_manager: Optional[ClientGameManager] = None

        self.error_message: Optional[arcade.gui.UILabel] = None

        # Client username
        username_text = arcade.gui.UILabel(text="Your username", font_name=FONT_NAME, text_color=CONTRAST_COLOR)
        self.v_box.add(username_text.with_space_around(bottom=TINY_PADDING))
        username_input = arcade.gui.UIInputText(text="Guest",
                                                font_name=FONT_NAME,
                                                font_size=NORMAL_FONT_SIZE,
                                                width=INPUT_TEXT_WIDTH,
                                                text_color=INPUT_COLOR)
        self.v_box.add(username_input.with_space_around(bottom=NORMAL_PADDING))

        # Server IP
        ip_text = arcade.gui.UILabel(text="The server IP", font_name=FONT_NAME, text_color=CONTRAST_COLOR)
        self.v_box.add(ip_text.with_space_around(bottom=TINY_PADDING))
        ip_input = arcade.gui.UIInputText(text="192.168.1.29",
                                          font_name=FONT_NAME,
                                          font_size=NORMAL_FONT_SIZE,
                                          width=INPUT_TEXT_WIDTH,
                                          text_color=INPUT_COLOR)
        self.v_box.add(ip_input.with_space_around(bottom=NORMAL_PADDING))

        # Server port
        port_text = arcade.gui.UILabel(text="The server port", font_name=FONT_NAME, text_color=CONTRAST_COLOR)
        self.v_box.add(port_text.with_space_around(bottom=TINY_PADDING))
        port_input = arcade.gui.UIInputText(text="9888",
                                            font_name=FONT_NAME,
                                            font_size=NORMAL_FONT_SIZE,
                                            width=INPUT_TEXT_WIDTH,
                                            text_color=INPUT_COLOR)
        self.v_box.add(port_input.with_space_around(bottom=NORMAL_PADDING))

        # Connect button
        connect_button = arcade.gui.UIFlatButton(text="Connect", width=BUTTON_WIDTH, style=BUTTON_STYLE)
        self.v_box.add(connect_button.with_space_around(bottom=NORMAL_PADDING))

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

        @connect_button.event("on_click")
        def __on_click_connect(event):

            # Get username, server IP and port
            ipv4_regex = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
            port_regex = re.compile(
                r'\b(?:[0-9]|[1-9][0-9]{1,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])\b')

            # If IP number incorrect, draw error label
            if not ipv4_regex.match(ip_input.text.strip()):
                self.show_error_label("Server IP incorrect")
                return

            # If port number incorrect, draw error label
            if not port_regex.match(port_input.text.strip()):
                self.show_error_label("Server port incorrect")
                return

            self.client_game_manager = ClientGameManager(username_input.text.strip(),
                                                         ip_input.text.strip(),
                                                         int(port_input.text.strip()))

            try:
                self.client_game_manager.initialize_session()

            except IOError as e:

                # If connection was not made, draw error label
                self.show_error_label("Connection error")
                return

            # Clear the screen and draw label about waiting for game start
            self.v_box.clear()
            self.error_message = False

            waiting_text = arcade.gui.UILabel(text="Waiting for game to start...",
                                              font_name=FONT_NAME,
                                              text_color=MAIN_COLOR,
                                              align="center")
            self.v_box.add(waiting_text.with_space_around(bottom=BIG_PADDING))

    def show_error_label(self, error_content: str):
        # Remove old error message if it exists
        if self.error_message:
            self.v_box.remove(self.error_message)

        self.error_message = arcade.gui.UILabel(text=error_content,
                                                font_name=FONT_NAME,
                                                font_size=ERROR_FONT_SIZE,
                                                text_color=ERROR_COLOR).with_space_around(bottom=TINY_PADDING)
        self.v_box.add(self.error_message)

    def on_update(self, delta_time: float):
        """
            Called every game frame.
            Checks for incoming game start message
        """

        if self.client_game_manager:
            # checking if game has been initialized (waiting for server to allow it)
            if not self.client_game_manager.check_if_should_initialize_game():
                return

            # start game
            rack = self.client_game_manager.initialize_game()
            self.__show_game_view(rack)

    def __show_game_view(self, rack):
        game_view = GameView(ClientActor(Board(), rack, self.client_game_manager.client))
        self.manager.disable()
        self.manager.clear()
        self.window.show_view(game_view)

    def on_key_press(self, key, modifiers):
        """
            Called every key press.
            When CTRL+V is pressed, clears selected text and pastes text from clipboard
        """

        if key == arcade.key.V and (modifiers & arcade.key.MOD_CTRL):
            pasted_text = paste()
            if isinstance(pasted_text, str):
                _clear_selected_text()
                typewrite(pasted_text)

    def on_draw(self):
        self.clear()
        self.manager.draw()


def _clear_selected_text():
    """
        Primitive method of deleting the contents of the selected text.
    """

    # Click the home button
    press('home')

    # Press Ctrl + Shift + End
    press('ctrl')
    press('shift')
    press('end')
    release('ctrl')
    release('shift')
    release('end')

    # Click the delete key
    press('delete')
