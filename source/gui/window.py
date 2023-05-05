import arcade
import arcade.gui

from ..manager.client_game_manager import ClientGameManager
from ..manager.server_game_manager import ServerGameManager

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Rummikub"


def on_click_exit(event):
    """
    Closes the app.
    """
    arcade.exit()


class Window(arcade.Window):
    """
    Main gui class.
    """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)

        # --- Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Set background
        arcade.set_background_color(arcade.color.AMAZON)

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
        exit_button.on_click = on_click_exit

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_click_join(self, event):
        self.manager.clear()
        # ClientGameManager().play()

    def on_click_host(self, event):
        self.manager.clear()
        # ServerGameManager().play()

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here
        pass

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()
        self.manager.draw()
