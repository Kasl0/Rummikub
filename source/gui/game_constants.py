from arcade import color

# Constants for sizing
TILE_SCALE = 0.6

# How big are the tiles
TILE_WIDTH = 100 * TILE_SCALE
TILE_HEIGHT = 160 * TILE_SCALE

TILE_CORNER_RADIUS = 10

TILE_BACKGROUND_COLOR = color.BEIGE

# How big is the board we'll place the tiles on
MAT_PERCENT_OVERSIZE = 1.25
MAT_HEIGHT = TILE_HEIGHT * MAT_PERCENT_OVERSIZE
MAT_WIDTH = TILE_WIDTH * MAT_PERCENT_OVERSIZE

# How much space do we leave as a gap between the tiles
# Done as a percent of the tile size.
VERTICAL_MARGIN_PERCENT = 0.10
HORIZONTAL_MARGIN_PERCENT = 0.10

# The Y of the bottom row (2 piles)
BOTTOM_Y = MAT_HEIGHT / 2 + MAT_HEIGHT * VERTICAL_MARGIN_PERCENT

# The X of where to start putting things on the left side
START_X = MAT_WIDTH / 2 + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT
