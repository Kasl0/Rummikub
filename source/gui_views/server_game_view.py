import arcade.gui
from arcade.gui import UIManager

from source.manager.server_game_manager import ServerGameManager
from source.gui_views.view_constants import *


class ServerGameView(arcade.View):

    def __init__(self, server_game_manager: ServerGameManager):
        super().__init__()
        self.server_game_manager = server_game_manager

        self.manager = UIManager()
        self.manager.enable()

        self.scroll_view = arcade.gui.UITextArea(text="Game has started\n", font_size=SMALL_FONT_SIZE, text_color=MAIN_COLOR, align="left", width=SCREEN_WIDTH, height=SCREEN_HEIGHT)

        self.manager.add(self.scroll_view.with_space_around(bottom=TINY_PADDING))

    def on_update(self, delta_time: float):
        """
            Called every game frame.
        """

        received_message = self.server_game_manager.update_main_game()
        if received_message:
            self.scroll_view.text += received_message.__str__() + "\n"
        if self.server_game_manager.game_has_ended():
            arcade.exit()

    def on_draw(self):
        self.clear()
        self.manager.draw()
