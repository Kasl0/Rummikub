import arcade

from .game_constants import *


def draw_rounded_rectangle_filled(center_x, center_y, width, height, corner_radius, color):
    # Calculate the positions of the rectangle's corners
    left = center_x - width / 2
    right = center_x + width / 2
    top = center_y + height / 2
    bottom = center_y - height / 2

    # Draw the rectangle body using polygons
    points = [
        (left + corner_radius, top),
        (right - corner_radius, top),
        (right, top - corner_radius),
        (right, bottom + corner_radius),
        (right - corner_radius, bottom),
        (left + corner_radius, bottom),
        (left, bottom + corner_radius),
        (left, top - corner_radius),
    ]
    arcade.draw_polygon_filled(points, color)

    # Draw circles at the corners to make them rounded
    arcade.draw_circle_filled(left + corner_radius, top - corner_radius, corner_radius, color)
    arcade.draw_circle_filled(right - corner_radius, top - corner_radius, corner_radius, color)
    arcade.draw_circle_filled(left + corner_radius, bottom + corner_radius, corner_radius, color)
    arcade.draw_circle_filled(right - corner_radius, bottom + corner_radius, corner_radius, color)


class GameTile:
    def __init__(self, tile, x, y):
        self.tile = tile
        self.color = tile.color.get_arcade_color()
        self.background_color = TILE_BACKGROUND_COLOR
        self.value = tile.value
        self.x = x
        self.y = y
        self.is_new = False
        self.is_dragging = False

    def draw(self):

        # Draw the tile as a rectangle
        draw_rounded_rectangle_filled(self.x, self.y, TILE_WIDTH, TILE_HEIGHT, TILE_CORNER_RADIUS, self.background_color)

        # Draw the value on the tile
        arcade.draw_text(str(self.value), self.x, self.y + TILE_HEIGHT/7, self.color, font_size=TILE_FONT_SIZE, anchor_x="center", anchor_y="center", bold=True)

    def is_hovering(self, x, y, over_mat=False):

        # Check if the mouse pointer is hovering over the mat
        if over_mat:
            return abs(x - self.x) < MAT_WIDTH / 2 and abs(y - self.y) < MAT_HEIGHT / 2

        # Check if the mouse pointer is hovering over the tile
        else:
            return abs(x - self.x) < TILE_WIDTH / 2 and abs(y - self.y) < TILE_HEIGHT / 2

    def start_dragging(self):
        self.background_color = TILE_BACKGROUND_COLOR
        self.is_dragging = True

    def stop_dragging(self):
        self.is_dragging = False

    def update_position(self, x, y):
        if self.is_dragging:
            self.x = x
            self.y = y

    def mark_as_new(self):
        self.is_new = True

    def unmark_as_new(self):
        self.is_new = False

    def mark_wrong_placed(self):
        self.background_color = WRONGLY_PLACED_TILE_BACKGROUND_COLOR
