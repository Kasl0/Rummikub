import arcade
import arcade.gui

from .start_screen import StartScreen

# Screen title and size
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Rummikub"


class App(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)

        # --- Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Set background
        arcade.set_background_color(arcade.color.AMAZON)

        # Initialize array with observers with callback function on game frame update and draw
        self.update_observers = []
        self.draw_observers = []

        # Display start screen
        StartScreen(self)

    def add_draw_observer(self, observer):
        self.draw_observers.append(observer)

    def remove_draw_observer(self, observer):
        self.draw_observers.remove(observer)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()
        self.manager.draw()

        for observer in self.draw_observers:
            observer.on_draw()

    def add_update_observer(self, observer):
        self.update_observers.append(observer)

    def remove_update_observer(self, observer):
        self.update_observers.remove(observer)

    def on_update(self, delta_time: float):
        for observer in self.update_observers:
            observer.on_update(delta_time)
