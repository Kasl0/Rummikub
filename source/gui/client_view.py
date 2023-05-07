import arcade.gui

from ..manager.client_game_manager import ClientGameManager
from .constants import *


class ClientView(arcade.View):

    def __init__(self, app):

        super().__init__()
        self.app = app
        self.v_box = arcade.gui.UIBoxLayout()
        self.v_box.align = "left"

        self.client_game_manager = None

        # Boolean attribute that informs whether error message is already displayed or not
        self.error_message = False

        # Client username
        username_text = arcade.gui.UILabel(text="Your username", font_name=FONT_NAME, text_color=CONTRAST_COLOR)
        self.v_box.add(username_text.with_space_around(bottom=TINY_PADDING))
        username_input = arcade.gui.UIInputText(text="Guest", font_name=FONT_NAME, font_size=NORMAL_FONT_SIZE, width=INPUT_TEXT_WIDTH, text_color=INPUT_COLOR)
        self.v_box.add(username_input.with_space_around(bottom=NORMAL_PADDING))

        # Server IP
        ip_text = arcade.gui.UILabel(text="The server IP", font_name=FONT_NAME, text_color=CONTRAST_COLOR)
        self.v_box.add(ip_text.with_space_around(bottom=TINY_PADDING))
        ip_input = arcade.gui.UIInputText(text="192.168.1.28", font_name=FONT_NAME, font_size=NORMAL_FONT_SIZE, width=INPUT_TEXT_WIDTH, text_color=INPUT_COLOR)
        self.v_box.add(ip_input.with_space_around(bottom=NORMAL_PADDING))

        # Server port
        port_text = arcade.gui.UILabel(text="The server port", font_name=FONT_NAME, text_color=CONTRAST_COLOR)
        self.v_box.add(port_text.with_space_around(bottom=TINY_PADDING))
        port_input = arcade.gui.UIInputText(text="1234", font_name=FONT_NAME, font_size=NORMAL_FONT_SIZE, width=INPUT_TEXT_WIDTH, text_color=INPUT_COLOR)
        self.v_box.add(port_input.with_space_around(bottom=NORMAL_PADDING))

        # Connect button
        connect_button = arcade.gui.UIFlatButton(text="Connect", width=BUTTON_WIDTH, style=BUTTON_STYLE)
        self.v_box.add(connect_button.with_space_around(bottom=NORMAL_PADDING))

        self.app.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

        @connect_button.event("on_click")
        def __on_click_connect(event):

            # Get username, server IP and port

            # TODO: Verify here whether the server IP is correct
            #  (is string with correct structure: 4 numbers 0-255 and 3 dots between them, no spaces)
            #  and if not draw error label

            # TODO: Verify here whether the server port is correct (is not a number) and if not draw error label

            self.client_game_manager = ClientGameManager(username_input.text, ip_input.text, int(port_input.text))

            try:
                self.client_game_manager.session_initialization()

            # handle the case where the connection was not made
            except IOError as e:

                # If connection was not made, draw error label
                if not self.error_message:
                    error_text = arcade.gui.UILabel(text="Connection error", font_name=FONT_NAME, font_size=ERROR_FONT_SIZE, text_color=ERROR_COLOR)
                    self.v_box.add(error_text.with_space_around(bottom=TINY_PADDING))
                    self.error_message = True
                return

            # Clear the screen and draw label about waiting for game start
            self.v_box.clear()
            self.error_message = False

            waiting_text = arcade.gui.UILabel(text="Waiting for game to start...", font_name=FONT_NAME, text_color=MAIN_COLOR, align="center")
            self.v_box.add(waiting_text.with_space_around(bottom=BIG_PADDING))

    def on_update(self, delta_time: float):
        """
            Called every game frame.
            Checks for incoming game start message
        """

        # checking for game start message
        if self.client_game_manager:
            return_value = self.client_game_manager.client.receive()

            # if start message
            if return_value:

                # Clear the screen
                self.v_box.clear()
                self.clear()

                # Initialise the game
                game_view = self.client_game_manager.game_initialization()
                self.window.show_view(game_view)
