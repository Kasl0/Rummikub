from arcade.gui import UIManager

from source.gui_views.client_view import ClientView
from source.gui_views.server_lobby_view import ServerLobbyView
from source.gui_views.view_constants import *


class StartView(arcade.View):
    def __init__(self):

        super().__init__()
        # self.app = arcade.Window
        self.manager = UIManager()
        self.manager.enable()

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Create the title
        title = arcade.gui.UILabel(text="Rummikub",
                                   align="center",
                                   font_size=TITLE_FONT_SIZE,
                                   font_name=FONT_NAME,
                                   text_color=MAIN_COLOR)
        self.v_box.add(title.with_space_around(bottom=BIG_PADDING))

        # Create the buttons
        join_button = arcade.gui.UIFlatButton(text="Join Game", width=BUTTON_WIDTH, style=BUTTON_STYLE)
        self.v_box.add(join_button.with_space_around(bottom=NORMAL_PADDING))

        host_button = arcade.gui.UIFlatButton(text="Host Game", width=BUTTON_WIDTH, style=BUTTON_STYLE)
        self.v_box.add(host_button.with_space_around(bottom=NORMAL_PADDING))

        exit_button = arcade.gui.UIFlatButton(text="Exit", width=BUTTON_WIDTH, style=BUTTON_STYLE)
        self.v_box.add(exit_button.with_space_around(bottom=NORMAL_PADDING))

        join_button.on_click = self.__on_click_join
        host_button.on_click = self.__on_click_host
        exit_button.on_click = self.__on_click_exit

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def __on_click_join(self, event):
        """
        Opens client screen.
        """
        self.manager.disable()
        self.manager.clear()
        client_view = ClientView()
        self.window.show_view(client_view)

    def __on_click_host(self, event):
        """
        Opens server screen.
        """
        self.manager.disable()
        self.manager.clear()
        server_view = ServerLobbyView()
        self.window.show_view(server_view)

    def __on_click_exit(self, event):
        """
        Closes the app.
        """
        self.manager.disable()
        arcade.exit()

    def on_draw(self):
        self.clear()
        self.manager.draw()
