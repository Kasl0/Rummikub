import arcade
import arcade.gui

from ..manager.server_game_manager import ServerGameManager
from ..conection.server import get_server_ip


class ServerScreen:

    button_style = {
        "font_name": "Kenney Future",
        "font_color": arcade.color.LIGHT_GRAY
    }

    def __init__(self, app):

        self.app = app
        self.v_box = arcade.gui.UIBoxLayout()
        self.v_box.align = "left"

        self.server_game_manager = None

        # Server IP
        ip_text = arcade.gui.UILabel(text="The server IP", width=400, font_name="Kenney Future", text_color=arcade.color.LIGHT_GRAY)
        self.v_box.add(ip_text.with_space_around(bottom=5))
        ip = arcade.gui.UILabel(text=get_server_ip(), width=400, font_name="Kenney Future", font_size=20, text_color=arcade.color.SMOKY_BLACK)
        self.v_box.add(ip.with_space_around(bottom=20))

        # Server port
        port_text = arcade.gui.UILabel(text="The server port", width=400, font_name="Kenney Future", text_color=arcade.color.LIGHT_GRAY)
        self.v_box.add(port_text.with_space_around(bottom=5))
        port_input = arcade.gui.UIInputText(text="1234", width=400, font_name="Kenney Future", font_size=20)
        self.v_box.add(port_input.with_space_around(bottom=20))

        # Start server button
        start_button = arcade.gui.UIFlatButton(text="Start", width=200, style=self.button_style)
        self.v_box.add(start_button.with_space_around(bottom=20))

        self.app.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

        @start_button.event("on_click")
        def on_click_start(event):
            # Lobby
            self.v_box.clear()

            lobby_text = arcade.gui.UILabel(text="Game lobby is now open", width=500, font_name="Kenney Future", font_size=20, text_color=arcade.color.SMOKY_BLACK)
            self.v_box.add(lobby_text.with_space_around(bottom=5))

            waiting_text = arcade.gui.UILabel(text="Waiting for players...", width=500, font_name="Kenney Future", text_color=arcade.color.SMOKY_BLACK)
            self.v_box.add(waiting_text.with_space_around(bottom=40))

            # Start game button
            play_button = arcade.gui.UIFlatButton(text="Play", width=200, style=self.button_style)
            self.v_box.add(play_button.with_space_around(bottom=40))

            @play_button.event("on_click")
            def on_click_play(event):
                self.server_game_manager.play()

            self.server_game_manager = ServerGameManager(int(port_input.text))

            self.app.add_update_observer(self)

    def on_update(self, delta_time: float):

        # checking for incoming connections
        return_value = self.server_game_manager.server.check_for_incoming_connections()

        # if new connection was made
        if return_value:

            # check if is the first client
            if self.server_game_manager.server.get_clients_count() == 1:

                # draw label for connected clients
                connected_text = arcade.gui.UILabel(text="Connected players:", width=500, font_name="Kenney Future", text_color=arcade.color.SMOKY_BLACK)
                self.v_box.add(connected_text.with_space_around(bottom=10))

            # add new client label
            client_username, client_address, assigned_client_id = return_value
            new_client_text = arcade.gui.UILabel(text=client_username, width=500, font_name="Kenney Future", text_color=arcade.color.SMOKY_BLACK, font_size=20)
            self.v_box.add(new_client_text.with_space_around(bottom=10))
