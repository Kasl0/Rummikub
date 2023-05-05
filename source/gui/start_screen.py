import arcade
import arcade.gui

from .client_screen import ClientScreen
from .server_screen import ServerScreen


class StartScreen:
    def __init__(self, app):

        self.app = app

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Create the title
        title = arcade.gui.UILabel(text="Rummikub",
                                   align="center",
                                   font_size=40,
                                   font_name="Kenney Future",
                                   text_color=arcade.color.SMOKY_BLACK)
        self.v_box.add(title.with_space_around(bottom=40))

        # Create the buttons

        button_style = {
            "font_name": "Kenney Future",
            "font_color": arcade.color.LIGHT_GRAY
        }

        join_button = arcade.gui.UIFlatButton(text="Join Game", width=200, style=button_style)
        self.v_box.add(join_button.with_space_around(bottom=20))

        host_button = arcade.gui.UIFlatButton(text="Host Game", width=200, style=button_style)
        self.v_box.add(host_button.with_space_around(bottom=20))

        exit_button = arcade.gui.UIFlatButton(text="Exit", width=200, style=button_style)
        self.v_box.add(exit_button.with_space_around(bottom=20))

        join_button.on_click = self.on_click_join
        host_button.on_click = self.on_click_host
        exit_button.on_click = self.on_click_exit

        # Create a widget to hold the v_box widget, that will center the buttons
        self.app.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_click_join(self, event):
        """
        Opens client screen.
        """
        self.app.manager.clear()
        ClientScreen(self.app)

    def on_click_host(self, event):
        """
        Opens server screen.
        """
        self.app.manager.clear()
        ServerScreen(self.app)

    def on_click_exit(self, event):
        """
        Closes the app.
        """
        arcade.exit()
