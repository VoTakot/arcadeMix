import arcade

SCREEN_HEIGHT = 1000
SCREEN_WIDTH = 1000
SCREEN_TITLE = 'Snake'


class Snake(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height, SCREEN_TITLE)
        self.width = width
        self.height = height
        self.game_over = False

    def update(self):
        pass

    def on_draw(self):
        pass


def setup_game(width=1000, height=600):
    game = Snake(width, height)
    game.setup()
    return game
