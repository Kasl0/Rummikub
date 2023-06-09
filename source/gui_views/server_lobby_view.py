import re
from time import sleep
from typing import Optional

import arcade.gui
from pyperclip import copy

from source.gui_views.server_game_view import ServerGameView
from source.manager.server_game_manager import ServerGameManager
from source.conection.server import get_server_ip
from source.gui_views.view_constants import *


class ServerLobbyView(arcade.View):

    def __init__(self):

        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.v_box = arcade.gui.UIBoxLayout()
        self.v_box.align = "left"

        self.server_game_manager: Optional[ServerGameManager] = None

        self.error_message: Optional[arcade.gui.UILabel] = None

        # Server IP
        ip_text = arcade.gui.UILabel(text="The server IP", font_name=FONT_NAME, text_color=CONTRAST_COLOR, width=COPY_BUTTON_GAP)
        self.v_box.add(ip_text.with_space_around(bottom=TINY_PADDING))
        ip = arcade.gui.UILabel(text=get_server_ip(), font_name=FONT_NAME, font_size=NORMAL_FONT_SIZE, text_color=MAIN_COLOR)
        self.v_box.add(ip.with_space_around(bottom=NORMAL_PADDING))

        # Server port
        port_text = arcade.gui.UILabel(text="The server port", font_name=FONT_NAME, text_color=CONTRAST_COLOR, width=COPY_BUTTON_GAP)
        self.v_box.add(port_text.with_space_around(bottom=TINY_PADDING))
        port_input = arcade.gui.UIInputText(text="9888", font_name=FONT_NAME, font_size=NORMAL_FONT_SIZE, width=INPUT_TEXT_WIDTH, text_color=INPUT_COLOR)
        self.v_box.add(port_input.with_space_around(bottom=NORMAL_PADDING))

        # Start server button
        start_button = arcade.gui.UIFlatButton(text="Start", width=BUTTON_WIDTH, style=BUTTON_STYLE)
        self.v_box.add(start_button.with_space_around(bottom=NORMAL_PADDING))

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

        @start_button.event("on_click")
        def __on_click_start(event):

            # TODO: Verify here whether the server port is correct and if not draw error label

            port_regex = re.compile(
                r'\b(?:[0-9]|[1-9][0-9]{1,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])\b')

            # If port number incorrect, draw error label
            if not port_regex.match(port_input.text.strip()):
                self.show_error_label("Server port incorrect")
                return

            port_number = int(port_input.text.strip())
            self.server_game_manager = ServerGameManager(port_number)

            self.v_box.clear()
            self.error_message = False

            # Server IP
            ip_h_box = arcade.gui.UIBoxLayout(vertical=False)
            ip_v_box = arcade.gui.UIBoxLayout(align="left")

            ip_v_box.add(ip_text.with_space_around(bottom=TINY_PADDING))
            ip_v_box.add(ip.with_space_around())

            ip_h_box.add(ip_v_box.with_space_around(right=BIG_PADDING))

            ip_copy_button = arcade.gui.UIFlatButton(text="Copy", width=COPY_BUTTON_WIDTH, style=BUTTON_STYLE)
            ip_h_box.add(ip_copy_button.with_space_around())

            self.v_box.add(ip_h_box.with_space_around(bottom=NORMAL_PADDING))

            @ip_copy_button.event("on_click")
            def __on_click_ip_copy(event):
                copy(ip.text)

            # Server port
            port_h_box = arcade.gui.UIBoxLayout(vertical=False)
            port_v_box = arcade.gui.UIBoxLayout(align="left")

            port_v_box.add(port_text.with_space_around(bottom=TINY_PADDING))
            port = arcade.gui.UILabel(text=str(port_number), font_name=FONT_NAME, font_size=NORMAL_FONT_SIZE, text_color=MAIN_COLOR)
            port_v_box.add(port.with_space_around())

            port_h_box.add(port_v_box.with_space_around(right=BIG_PADDING))

            port_copy_button = arcade.gui.UIFlatButton(text="Copy", width=COPY_BUTTON_WIDTH, style=BUTTON_STYLE)
            port_h_box.add(port_copy_button.with_space_around())

            self.v_box.add(port_h_box.with_space_around(bottom=BIG_PADDING * 2))

            @port_copy_button.event("on_click")
            def __on_click_port_copy(event):
                copy(str(port_number))

            # Lobby
            lobby_text = arcade.gui.UILabel(text="Game lobby is now open", font_name=FONT_NAME, font_size=NORMAL_FONT_SIZE, text_color=MAIN_COLOR)
            self.v_box.add(lobby_text.with_space_around(bottom=TINY_PADDING))

            waiting_text = arcade.gui.UILabel(text="Waiting for players...", font_name=FONT_NAME, text_color=MAIN_COLOR)
            self.v_box.add(waiting_text.with_space_around(bottom=BIG_PADDING))

            # Start game button
            play_button = arcade.gui.UIFlatButton(text="Play", width=BUTTON_WIDTH, style=BUTTON_STYLE)
            self.v_box.add(play_button.with_space_around(bottom=NORMAL_PADDING))

            @play_button.event("on_click")
            def __on_click_play(event):

                # Check if is there is at least 1 player
                if self.server_game_manager.server.get_clients_count() == 0:

                    # If there are not enough players, draw error label
                    if not self.error_message:
                        no_enough_text = arcade.gui.UILabel(text="Not enough players", font_name=FONT_NAME, font_size=ERROR_FONT_SIZE, text_color=ERROR_COLOR)
                        self.v_box.add(no_enough_text.with_space_around(bottom=TINY_PADDING))
                        self.error_message = True
                    return

                # Clear the screen and draw label about started game
                self.v_box.clear()

                started_text = arcade.gui.UILabel(text="Game has started", font_name=FONT_NAME, font_size=NORMAL_FONT_SIZE, text_color=MAIN_COLOR, align="center")
                self.v_box.add(started_text.with_space_around(bottom=TINY_PADDING))

                self.on_draw()

                # Start the game
                self.server_game_manager.session_initialization()
                sleep(1)  # TODO: Not very professional (but works)
                self.server_game_manager.game_initialization()

                self.__show_server_game_view()

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
            Checks for incoming connections and if there is a new one, adds new player to the game lobby.
        """

        # checking for incoming connections
        if self.server_game_manager:
            return_value = self.server_game_manager.server.check_for_incoming_connections()

            # if new connection was made
            if return_value:

                if self.error_message:

                    # Remove error message label
                    self.v_box.children.pop(len(self.v_box.children)-1)
                    self.error_message = False

                # check if new connection is the first one
                if self.server_game_manager.server.get_clients_count() == 1:

                    # draw label for connected clients
                    connected_text = arcade.gui.UILabel(text="Connected players:", font_name=FONT_NAME, text_color=MAIN_COLOR)
                    self.v_box.add(connected_text.with_space_around(bottom=SMALL_PADDING))

                # add new client label
                client_username, client_address, assigned_client_id = return_value
                new_client_text = arcade.gui.UILabel(text=client_username, font_name=FONT_NAME, text_color=MAIN_COLOR, font_size=NORMAL_FONT_SIZE)
                self.v_box.add(new_client_text.with_space_around(bottom=SMALL_PADDING))

    def __show_server_game_view(self):
        server_game_view = ServerGameView(self.server_game_manager)
        self.manager.disable()
        self.manager.clear()
        self.window.show_view(server_game_view)

    def on_draw(self):
        self.clear()
        self.manager.draw()
