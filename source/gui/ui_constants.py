import arcade
from .game_constants import BOARD_WIDTH, BOARD_HEIGHT, GAP, RACK_HEIGHT

# Screen title and size
SCREEN_TITLE = "Rummikub"
SCREEN_WIDTH = int(BOARD_WIDTH)
SCREEN_HEIGHT = int(BOARD_HEIGHT + RACK_HEIGHT + GAP)


# Font
FONT_NAME = "Kenney Future"

TITLE_FONT_SIZE = 40
NORMAL_FONT_SIZE = 20
ERROR_FONT_SIZE = 15

MAIN_COLOR = arcade.color.EERIE_BLACK       # for user non editable labels
INPUT_COLOR = arcade.color.BLACK            # for user editable labels
CONTRAST_COLOR = arcade.color.LIGHT_GRAY
ERROR_COLOR = arcade.color.CARMINE


# Padding
BIG_PADDING = 40
NORMAL_PADDING = 20
SMALL_PADDING = 10
TINY_PADDING = 5


# Buttons
BUTTON_WIDTH = 200

BUTTON_STYLE = {
    "font_name": FONT_NAME,
    "font_color": CONTRAST_COLOR
}


# Input text
INPUT_TEXT_WIDTH = 400


# Background
BACKGROUND_COLOR = arcade.color.AMAZON
