from arcade import color

# Constants for sizing
SCALE = 0.5

# How big are the tiles
TILE_WIDTH = 100 * SCALE
TILE_HEIGHT = 160 * SCALE
TILE_FONT_SIZE = 60 * SCALE

TILE_CORNER_RADIUS = 10 * SCALE

TILE_BACKGROUND_COLOR = color.BABY_POWDER

# How big are the board cells we'll place the tiles on
MAT_PERCENT_OVERSIZE = 1.05
MAT_HEIGHT = TILE_HEIGHT * MAT_PERCENT_OVERSIZE
MAT_WIDTH = TILE_WIDTH * MAT_PERCENT_OVERSIZE


# Set how many board rows and columns we will have
BOARD_ROW_COUNT = 8
BOARD_COLUMN_COUNT = 22

BOARD_HEIGHT = BOARD_ROW_COUNT * MAT_HEIGHT
BOARD_WIDTH = BOARD_COLUMN_COUNT * MAT_WIDTH

# Set board colors
BOARD_GRID_COLOR = color.CHARLESTON_GREEN
BOARD_BACKGROUND_COLOR = color.BLUE_SAPPHIRE

# Set gap between board and rack
GAP = 100 * SCALE

# Set how many rack rows and columns we will have
RACK_ROW_COUNT = 2
RACK_COLUMN_COUNT = 15

RACK_HEIGHT = RACK_ROW_COUNT * MAT_HEIGHT
RACK_WIDTH = RACK_COLUMN_COUNT * MAT_WIDTH

# Set rack color
RACK_COLOR = color.COFFEE