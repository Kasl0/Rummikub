import arcade

from .gui.window import Window


def main():
    window = Window()
    window.setup()
    arcade.run()


if __name__ == '__main__':
    main()
