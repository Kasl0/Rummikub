import arcade

from ..logic.tile import Tile


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


class TileSprite:
    def __init__(self, color, value, width, height, x, y):
        self.color = color
        self.value = value
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.is_dragging = False

    """def draw(self):
        # Constants for sizing
        TILE_SCALE = 0.6
        TILE_WIDTH = 100 * TILE_SCALE
        TILE_HEIGHT = 160 * TILE_SCALE

        TILE_CORNER_RADIUS = 10
        # Draw the tile as a rectangle
        #draw_rounded_rectangle_filled(self.x, self.y, self.width, self.height, 10, arcade.color.BEIGE)

        # Draw the value on the tile
        # arcade.draw_text(str(self.value), self.x, self.y, self.color, font_size=30, anchor_x="center", anchor_y="center")

        # Draw the tile as a rectangle
        draw_rounded_rectangle_filled(self.x, self.y, TILE_WIDTH, TILE_HEIGHT, TILE_CORNER_RADIUS, arcade.color.BEIGE)

        # Draw the value on the tile
        arcade.draw_text(str(self.value), self.x, self.y, self.color, font_size=30, anchor_x="center",
                         anchor_y="center")"""

    def draw(self):
        # Draw the tile as a rectangle
        arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, arcade.color.BEIGE)

        # Draw the value on the tile
        arcade.draw_text(str(self.value), self.x, self.y, self.color, font_size=30, anchor_x="center",
                         anchor_y="center")

    def is_hovering(self, x, y):
        # Check if the mouse pointer is hovering over the tile
        return abs(x - self.x) < self.width / 2 and abs(y - self.y) < self.height / 2

    def start_dragging(self):
        self.is_dragging = True

    def stop_dragging(self):
        self.is_dragging = False

    def update_position(self, x, y):
        if self.is_dragging:
            self.x = x
            self.y = y
