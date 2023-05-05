import arcade
import arcade.gui

from ..manager.client_game_manager import ClientGameManager


class ClientScreen:

    button_style = {
        "font_name": "Kenney Future",
        "font_color": arcade.color.LIGHT_GRAY
    }

    def __init__(self, app):

        self.app = app
        self.v_box = arcade.gui.UIBoxLayout()
        self.v_box.align = "left"

        self.client_game_manager = None

        # Client username
        username_text = arcade.gui.UILabel(text="Your username", width=400, font_name="Kenney Future", text_color=arcade.color.LIGHT_GRAY)
        self.v_box.add(username_text.with_space_around(bottom=5))
        username_input = arcade.gui.UIInputText(text="Guest", width=400, font_name="Kenney Future", font_size=20)
        self.v_box.add(username_input.with_space_around(bottom=20))

        # Server IP
        ip_text = arcade.gui.UILabel(text="The server IP", width=400, font_name="Kenney Future", text_color=arcade.color.LIGHT_GRAY)
        self.v_box.add(ip_text.with_space_around(bottom=5))
        ip_input = arcade.gui.UIInputText(text="192.168.1.28", width=400, font_name="Kenney Future", font_size=20)
        self.v_box.add(ip_input.with_space_around(bottom=20))

        # Server port
        port_text = arcade.gui.UILabel(text="The server port", width=400, font_name="Kenney Future", text_color=arcade.color.LIGHT_GRAY)
        self.v_box.add(port_text.with_space_around(bottom=5))
        port_input = arcade.gui.UIInputText(text="1234", width=400, font_name="Kenney Future", font_size=20)
        self.v_box.add(port_input.with_space_around(bottom=20))

        # Connect button
        connect_button = arcade.gui.UIFlatButton(text="Connect", width=200, style=self.button_style)
        self.v_box.add(connect_button.with_space_around(bottom=20))

        self.app.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

        @connect_button.event("on_click")
        def on_click_connect(event):
            self.client_game_manager = ClientGameManager(username_input.text, ip_input.text, int(port_input.text))
            self.client_game_manager.session_initialization()

            self.v_box.clear()

            waiting_text = arcade.gui.UILabel(text="Waiting for game to start...", width=500, font_name="Kenney Future", text_color=arcade.color.SMOKY_BLACK)
            self.v_box.add(waiting_text.with_space_around(bottom=40))

            self.app.add_update_observer(self)

    def on_update(self, delta_time: float):
        return_value = self.client_game_manager.client.receive()
        if return_value:
            print("Zaczynamy")
