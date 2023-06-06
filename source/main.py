import arcade

from source.gui_views.start_view import StartView
from source.gui_views.view_constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, BACKGROUND_COLOR


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=False)
    arcade.set_background_color(BACKGROUND_COLOR)

    # Display start screen
    start_view = StartView()
    window.show_view(start_view)

    # Run the application
    arcade.run()

if __name__ == '__main__':
    main()
