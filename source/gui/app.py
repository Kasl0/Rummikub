import arcade.gui

from .start_screen import StartScreen
from .ui_constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, BACKGROUND_COLOR


class App(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)

        # Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Set background
        arcade.set_background_color(BACKGROUND_COLOR)

        # Display start screen
        start_screen = StartScreen(self)
        self.show_view(start_screen)

    def on_draw(self):
        """
            Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()
        self.manager.draw()
