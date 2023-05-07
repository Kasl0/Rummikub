import arcade.gui

from ..manager.server_game_manager import ServerGameManager
from ..conection.server import get_server_ip
from .ui_constants import *


class ServerView(arcade.View):

    def __init__(self, app):

        super().__init__()
        self.app = app
        self.v_box = arcade.gui.UIBoxLayout()
        self.v_box.align = "left"

        self.server_game_manager = None

        # Boolean attribute that informs whether game has already started
        self.started = False

        # Boolean attribute that informs whether error message is already displayed
        self.error_message = False

        # Server IP
        ip_text = arcade.gui.UILabel(text="The server IP", font_name=FONT_NAME, text_color=CONTRAST_COLOR)
        self.v_box.add(ip_text.with_space_around(bottom=TINY_PADDING))
        ip = arcade.gui.UILabel(text=get_server_ip(), font_name=FONT_NAME, font_size=NORMAL_FONT_SIZE, text_color=MAIN_COLOR)
        self.v_box.add(ip.with_space_around(bottom=NORMAL_PADDING))

        # Server port
        port_text = arcade.gui.UILabel(text="The server port", font_name=FONT_NAME, text_color=CONTRAST_COLOR)
        self.v_box.add(port_text.with_space_around(bottom=TINY_PADDING))
        port_input = arcade.gui.UIInputText(text="1234", font_name=FONT_NAME, font_size=NORMAL_FONT_SIZE, width=INPUT_TEXT_WIDTH, text_color=INPUT_COLOR)
        self.v_box.add(port_input.with_space_around(bottom=NORMAL_PADDING))

        # Start server button
        start_button = arcade.gui.UIFlatButton(text="Start", width=BUTTON_WIDTH, style=BUTTON_STYLE)
        self.v_box.add(start_button.with_space_around(bottom=NORMAL_PADDING))

        self.app.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

        @start_button.event("on_click")
        def __on_click_start(event):

            # Get port number

            # TODO: Verify here whether the server port is correct (is not a number) and if not draw error label

            self.server_game_manager = ServerGameManager(int(port_input.text))

            # Lobby
            self.v_box.clear()

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

                self.started = True

                # Clear the screen and draw label about started game
                self.v_box.clear()

                started_text = arcade.gui.UILabel(text="Game has started", font_name=FONT_NAME, font_size=NORMAL_FONT_SIZE, text_color=MAIN_COLOR, align="center")
                self.v_box.add(started_text.with_space_around(bottom=TINY_PADDING))

                # Start the game
                self.server_game_manager.play()

    def on_update(self, delta_time: float):
        """
            Called every game frame.
            Checks for incoming connections and if there is a new one, adds new player to the game lobby.
        """

        # checking for incoming connections
        if self.server_game_manager and not self.started:
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
