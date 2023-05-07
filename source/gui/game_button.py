import arcade


class GameButton:
    def __init__(self, x, y, width, height, text, font_size=12, font_face="Kenney Future", bg_color=arcade.color.BLACK, text_color=arcade.color.LIGHT_GRAY):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size
        self.font_face = font_face
        self.bg_color = bg_color
        self.text_color = text_color

    def draw(self):
        arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, self.bg_color)
        arcade.draw_text(self.text, self.x, self.y, self.text_color, self.font_size, width=self.width, align="center", font_name=self.font_face, anchor_x="center", anchor_y="center", bold=True)

    def is_mouse_on_button(self, x, y):
        return (self.x - self.width / 2) < x < (self.x + self.width / 2) and (self.y - self.height / 2) < y < (self.y + self.height / 2)
