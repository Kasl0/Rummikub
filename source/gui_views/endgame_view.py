import arcade.gui

from source.gui_views.client_view import ClientView
from source.gui_views.server_lobby_view import ServerLobbyView
from source.gui_views.view_constants import *


class EndgameView(arcade.View):
    def __init__(self, app, winner_nickname):

        super().__init__()
        self.app = app

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Create the title
        title = arcade.gui.UILabel(text="The game has ended!",
                                   align="center",
                                   font_size=TITLE_FONT_SIZE,
                                   font_name=FONT_NAME,
                                   text_color=MAIN_COLOR)
        self.v_box.add(title.with_space_around(bottom=BIG_PADDING))

        winner_label1 = arcade.gui.UILabel(text="The winner is:",
                                   align="center",
                                   font_size=NORMAL_FONT_SIZE,
                                   font_name=FONT_NAME,
                                   text_color=MAIN_COLOR)
        self.v_box.add(winner_label1.with_space_around(bottom=BIG_PADDING))

        winner_label2 = arcade.gui.UILabel(text=winner_nickname,
                                          align="center",
                                          font_size=TITLE_FONT_SIZE,
                                          font_name=FONT_NAME,
                                          text_color=MAIN_COLOR)
        self.v_box.add(winner_label2.with_space_around(bottom=BIG_PADDING))

        # Create the button
        exit_button = arcade.gui.UIFlatButton(text="Exit", width=BUTTON_WIDTH, style=BUTTON_STYLE)
        self.v_box.add(exit_button.with_space_around(bottom=NORMAL_PADDING))

        exit_button.on_click = self.__on_click_exit

        # Create a widget to hold the v_box widget, that will center the buttons
        self.app.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def __on_click_exit(self, event):
        """
        Closes the app.
        """
        arcade.exit()
