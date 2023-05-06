import arcade.gui

from .start_screen import StartScreen
from .constants import *


class App(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)

        # Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Set background
        arcade.set_background_color(BACKGROUND_COLOR)

        # Initialize array with observers with callback function on game frame update and draw
        self.update_observers = []
        self.draw_observers = []

        # Display start screen
        StartScreen(self)

    def add_draw_observer(self, observer):
        """
            Adds observer to draw_observers list.
            Observer is now subscribed to app on_draw() callback.
            Observer MUST have on_draw() method implemented.
        """
        self.draw_observers.append(observer)

    def remove_draw_observer(self, observer):
        """
            Removes observer from draw_observers list.
            Observer is now unsubscribed from app on_draw() callback.
        """
        self.draw_observers.remove(observer)

    def on_draw(self):
        """
            Render the screen.
            Calls all draw_observers on_draw() methods.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()
        self.manager.draw()

        for observer in self.draw_observers:
            observer.on_draw()

    def add_update_observer(self, observer):
        """
            Adds observer to update_observers list.
            Observer is now subscribed to app on_update() callback.
            Observer MUST have on_update() method implemented.
        """
        self.update_observers.append(observer)

    def remove_update_observer(self, observer):
        """
            Removes observer from update_observers list.
            Observer is now unsubscribed from app on_update() callback.
        """
        self.update_observers.remove(observer)

    def on_update(self, delta_time: float):
        """
            Is being called every single game frame.
            Calls all update_observers on_update() methods.
        """
        for observer in self.update_observers:
            observer.on_update(delta_time)
